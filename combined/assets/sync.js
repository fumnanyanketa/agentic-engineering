// ---------------------------------------------------------------------------
// CourseSync: cross-device progress for Self-Paced CS50x.
//
// Signed out (or before Firebase is configured): progress is kept in this
// browser's localStorage, so the course still works fully offline.
// Signed in with Google: progress is stored in Firestore under your account and
// mirrored to every device you sign in on. localStorage stays as an offline
// cache, so the page paints instantly and queued writes sync when back online.
// ---------------------------------------------------------------------------
import { firebaseConfig } from "./sync-config.js";

const FB_VER = "10.12.0";
const LS_LESSONS = "agentic:progress";
const LS_PACE = "agentic:pace";

// Two sync backends, chosen in course.json:
//   "sync": {"provider": "firebase"}    Google sign-in + Firestore
//   "sync": {"provider": "cloudflare"}  a Pages Function behind Cloudflare
//                                       Access, which means NO second login:
//                                       Access already authenticated the
//                                       request, so the endpoint trusts it.
const SYNC = (typeof window !== "undefined" && window.COURSE_DATA && window.COURSE_DATA.sync) || {};
const CF_MODE = SYNC.provider === "cloudflare";
const CF_ENDPOINT = SYNC.endpoint || "/api/progress";
const CONFIGURED = CF_MODE ||
  !!(firebaseConfig && firebaseConfig.projectId && firebaseConfig.projectId !== "REPLACE_ME");

let user = null;
let auth = null, db = null, userDocRef = null, unsubDoc = null, fb = null;
const listeners = new Set();
let state = { lessons: loadLocalLessons(), pace: loadLocalPace() };

function loadLocalLessons() { try { return JSON.parse(localStorage.getItem(LS_LESSONS)) || {}; } catch (e) { return {}; } }
function loadLocalPace() { const p = parseInt(localStorage.getItem(LS_PACE) || "1", 10); return isNaN(p) ? 1 : p; }
function saveLocal() { localStorage.setItem(LS_LESSONS, JSON.stringify(state.lessons)); localStorage.setItem(LS_PACE, String(state.pace)); }
function emit() { listeners.forEach(fn => { try { fn(); } catch (e) {} }); }
function todayISO() { const d = new Date(); return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }
function daysBetween(a, b) { return Math.round((new Date(b + "T00:00") - new Date(a + "T00:00")) / 86400000); }

// Writes are debounced because Workers KV allows 1,000 writes a day on the
// free tier and ticking through a phase quickly would otherwise burn one per
// click. A second of quiet is plenty, and localStorage has already painted.
let cfWriteTimer = null;
function pushCloudflare() {
  clearTimeout(cfWriteTimer);
  cfWriteTimer = setTimeout(async () => {
    try {
      await fetch(CF_ENDPOINT, {
        method: "PUT",
        headers: { "content-type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify({ lessons: state.lessons, pace: state.pace }),
      });
    } catch (e) { /* offline: localStorage keeps it, next write catches up */ }
  }, 1000);
}

async function pushCloud() {
  if (CF_MODE) { pushCloudflare(); return; }
  if (user && userDocRef && fb) {
    try { await fb.setDoc(userDocRef, { lessons: state.lessons, pace: state.pace, updated: Date.now() }, { merge: true }); } catch (e) {}
  }
}

const CourseSync = {
  configured() { return CONFIGURED; },
  ready() { return true; },
  state() { return state; },
  user() { return user; },
  isDone(n) { return !!state.lessons[String(n)]; },
  dateOf(n) { return state.lessons[String(n)] || ""; },
  onChange(fn) { listeners.add(fn); return () => listeners.delete(fn); },
  // ---- shared progress stats (single source of truth for the bar + tracker) ----
  coreTotal() { return (window.COURSE_DATA && window.COURSE_DATA.coreTotal) || 43; },
  optionalIds() { return (window.COURSE_DATA && window.COURSE_DATA.optionalIds) || [0]; },
  coreDone() {
    const opt = new Set(this.optionalIds().map(String));
    return Object.keys(state.lessons).filter(k => !opt.has(String(k))).length;
  },
  streak() {
    const dates = [...new Set(Object.values(state.lessons))].sort();
    if (!dates.length) return 0;
    if (daysBetween(dates[dates.length - 1], todayISO()) > 1) return 0;
    let s = 1;
    for (let i = dates.length - 1; i > 0; i--) { if (daysBetween(dates[i - 1], dates[i]) === 1) s++; else break; }
    return s;
  },
  weekCount() {
    const t = todayISO();
    return Object.values(state.lessons).filter(d => { const n = daysBetween(d, t); return n >= 0 && n < 7; }).length;
  },
  stats() {
    const total = this.coreTotal();
    const done = Math.min(this.coreDone(), total);
    return { done, total, pct: total ? Math.round(done / total * 100) : 0, streak: this.streak(), week: this.weekCount() };
  },
  toggleLesson(n) { this.setLesson(n, !this.isDone(n)); },
  setLesson(n, done) {
    n = String(n);
    if (done) { if (!state.lessons[n]) state.lessons[n] = todayISO(); }
    else { delete state.lessons[n]; }
    saveLocal(); emit(); pushCloud();
  },
  setPace(p) { state.pace = p; saveLocal(); emit(); pushCloud(); },
  exportData() { return JSON.stringify(state.lessons); },
  importData(str) { try { const o = JSON.parse(str); if (o && typeof o === "object") { state.lessons = o; saveLocal(); emit(); pushCloud(); return true; } } catch (e) {} return false; },
  reset() { state.lessons = {}; saveLocal(); emit(); pushCloud(); },
  async signIn() {
    // Under Cloudflare Access there is nothing to sign in to: reaching this
    // page at all means you are already authenticated.
    if (CF_MODE) return;
    if (!CONFIGURED) { alert("Cross-device sync is not set up yet.\nAdd your Firebase config to assets/sync-config.js to enable sign-in."); return; }
    if (!auth || !fb) { alert("Still starting up. Try again in a second."); return; }
    try { await fb.signInWithPopup(auth, new fb.GoogleAuthProvider()); }
    catch (e) { alert("Sign-in failed: " + ((e && e.message) || e)); }
  },
  async signOut() {
    if (auth && fb) { try { await fb.signOut(auth); } catch (e) {} }
    user = null; state.lessons = loadLocalLessons(); emit();
  }
};
window.CourseSync = CourseSync;

// Cloudflare mode: read once on load, merge anything this browser did while
// offline, and let pushCloud() handle writes from then on.
async function initCloudflare() {
  try {
    const res = await fetch(CF_ENDPOINT, { credentials: "same-origin", headers: { "cache-control": "no-cache" } });
    if (!res.ok) { emit(); return; }
    const body = await res.json();
    if (body && body.user) user = { name: body.user, email: body.user, uid: body.user };
    const cloud = (body && body.data && body.data.lessons) || {};
    // Union of both sides. A session ticked anywhere counts as done, and the
    // earlier of two dates wins, so re-reading on a second device never
    // silently moves a completion date forward.
    let changed = false;
    for (const k in state.lessons) {
      if (!cloud[k] || state.lessons[k] < cloud[k]) { cloud[k] = state.lessons[k]; changed = true; }
    }
    state.lessons = cloud;
    if (body && body.data && typeof body.data.pace === "number") state.pace = body.data.pace;
    saveLocal(); emit();
    if (changed) pushCloudflare();
  } catch (e) {
    console.warn("CourseSync: progress endpoint unreachable, staying local-only.", e);
    emit();
  }
}

async function initFirebase() {
  if (CF_MODE) { initCloudflare(); return; }
  if (!CONFIGURED) { emit(); return; }
  try {
    const [appMod, authMod, fsMod] = await Promise.all([
      import(`https://www.gstatic.com/firebasejs/${FB_VER}/firebase-app.js`),
      import(`https://www.gstatic.com/firebasejs/${FB_VER}/firebase-auth.js`),
      import(`https://www.gstatic.com/firebasejs/${FB_VER}/firebase-firestore.js`)
    ]);
    const app = appMod.initializeApp(firebaseConfig);
    auth = authMod.getAuth(app);
    try { db = fsMod.initializeFirestore(app, { localCache: fsMod.persistentLocalCache({ tabManager: fsMod.persistentMultipleTabManager() }) }); }
    catch (e) { db = fsMod.getFirestore(app); }
    fb = {
      GoogleAuthProvider: authMod.GoogleAuthProvider,
      signInWithPopup: authMod.signInWithPopup,
      signOut: authMod.signOut,
      doc: fsMod.doc, onSnapshot: fsMod.onSnapshot, setDoc: fsMod.setDoc, getDoc: fsMod.getDoc
    };
    authMod.onAuthStateChanged(auth, async (u) => {
      if (unsubDoc) { unsubDoc(); unsubDoc = null; }
      user = u ? { name: u.displayName || u.email, email: u.email, uid: u.uid } : null;
      if (u) {
        userDocRef = fb.doc(db, "progress", u.uid);
        await mergeLocalIntoCloud();
        unsubDoc = fb.onSnapshot(userDocRef, (snap) => {
          const data = (snap && snap.data && snap.data()) || {};
          state.lessons = data.lessons || {};
          if (typeof data.pace === "number") state.pace = data.pace;
          saveLocal(); emit();
        });
      }
      emit();
    });
  } catch (e) {
    console.warn("CourseSync: Firebase init failed, staying in local-only mode.", e);
    emit();
  }
}

async function mergeLocalIntoCloud() {
  try {
    const snap = await fb.getDoc(userDocRef);
    const cloud = (snap.exists() ? (snap.data().lessons || {}) : {});
    let changed = false;
    for (const k in state.lessons) { if (!cloud[k]) { cloud[k] = state.lessons[k]; changed = true; } }
    if (!snap.exists() || changed) {
      await fb.setDoc(userDocRef, { lessons: cloud, pace: state.pace, updated: Date.now() }, { merge: true });
    }
  } catch (e) {}
}

// ---- auto-wire a "Mark this lesson complete" button on lesson pages ----
function paintBox(box) {
  const n = box.getAttribute("data-lesson-id");
  const btn = box.querySelector("[data-lesson-complete]");
  const status = box.querySelector("[data-sync-status]");
  const done = CourseSync.isDone(n);
  box.classList.toggle("done", done);
  if (btn) btn.textContent = done ? "✓  Completed (click to undo)" : "Mark this lesson complete";
  if (status) {
    if (!CourseSync.configured()) status.textContent = "saved in this browser";
    else if (!CourseSync.user()) status.innerHTML = '<a href="#" data-signin>Sign in to sync across your devices</a>';
    else status.textContent = "synced as " + (CourseSync.user().name || "you");
  }
}
function wireLessonButtons() {
  document.querySelectorAll("[data-lesson-id]").forEach(box => {
    const btn = box.querySelector("[data-lesson-complete]");
    if (btn && !btn._wired) { btn._wired = true; btn.addEventListener("click", () => CourseSync.toggleLesson(box.getAttribute("data-lesson-id"))); }
    paintBox(box);
  });
}
document.addEventListener("click", (e) => { const a = e.target.closest("[data-signin]"); if (a) { e.preventDefault(); CourseSync.signIn(); } });
CourseSync.onChange(() => document.querySelectorAll("[data-lesson-id]").forEach(paintBox));

// ---- styles for the lesson button (injected once) ----
const css = `
.lesson-sync{margin:38px 0 8px;padding:18px 20px;border:1px solid #1e3a5a;border-radius:14px;background:#0f243d;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.lesson-sync.done{background:linear-gradient(90deg,rgba(45,212,191,.12),#0f243d 60%);border-color:#2dd4bf}
.lesson-sync .ls-inner{display:flex;align-items:center;gap:14px;flex-wrap:wrap;flex:1 1 auto}
.lesson-sync .ls-btn{background:#2dd4bf;color:#05202a;border:0;border-radius:10px;padding:11px 18px;font:600 1rem system-ui,sans-serif;cursor:pointer}
.lesson-sync.done .ls-btn{background:#16324f;color:#e8eef6;border:1px solid #2dd4bf}
.lesson-sync .ls-btn:hover{filter:brightness(1.06)}
.lesson-sync .ls-status{color:#9fb3c8;font-size:.85rem}
.lesson-sync .ls-status a{color:#2dd4bf}
.lesson-sync .ls-track{color:#2dd4bf;font-size:.9rem;text-decoration:none;white-space:nowrap}
.lesson-sync .ls-track:hover{text-decoration:underline}`;
const st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

// ---- persistent course-progress bar on every lesson page ----
// Always-visible strip fixed to the bottom of the viewport so a learner never
// has to remember a separate tracker page: their standing is always on screen,
// and the whole bar links to the home page (which is the full tracker).
const barCss = `
#course-progress-bar{position:fixed;left:0;right:0;bottom:0;z-index:150;background:#0a1a2f;border-top:1px solid #1e3a5a;color:#e8eef6;display:flex;align-items:center;gap:14px;padding:9px 16px;font:600 .85rem system-ui,-apple-system,Segoe UI,Roboto,sans-serif;text-decoration:none;box-shadow:0 -6px 20px rgba(0,0,0,.28)}
#course-progress-bar:hover{background:#0c1f38}
#course-progress-bar .cpb-label{color:#9fb3c8;font-weight:600;white-space:nowrap}
#course-progress-bar .cpb-track{flex:1 1 auto;height:8px;background:#16324f;border-radius:999px;overflow:hidden;min-width:70px;max-width:360px}
#course-progress-bar .cpb-fill{display:block;height:100%;width:0;background:linear-gradient(90deg,#2dd4bf,#34d399);transition:width .4s ease}
#course-progress-bar .cpb-count{color:#2dd4bf;white-space:nowrap}
#course-progress-bar .cpb-pct{color:#e8eef6;white-space:nowrap}
#course-progress-bar .cpb-streak{color:#f5c451;white-space:nowrap}
#course-progress-bar .cpb-cta{margin-left:auto;color:#9fb3c8;white-space:nowrap}
#course-progress-bar:hover .cpb-cta{color:#2dd4bf}
@media(max-width:560px){#course-progress-bar .cpb-label{display:none}#course-progress-bar{gap:10px;padding:8px 12px;font-size:.8rem}}`;
function injectCourseBar() {
  // Renders on unit pages (which carry data-lesson-id) and on the home page,
  // which carries data-progress-home instead. One strip, every page.
  const box = document.querySelector("[data-lesson-id]");
  const isHome = !box && !!document.querySelector("[data-progress-home]");
  if (!box && !isHome) return;
  if (document.getElementById("course-progress-bar")) return;
  const D = window.COURSE_DATA || {};
  const label = D.progressLabel || "Course progress";
  const cta = D.progressCta || "View tracker";
  const bs = document.createElement("style"); bs.textContent = barCss; document.head.appendChild(bs);
  const bar = document.createElement(isHome ? "div" : "a");
  bar.id = "course-progress-bar";
  if (!isHome) bar.href = box.getAttribute("data-home") || "../index.html";
  bar.innerHTML =
    '<span class="cpb-label">' + label + '</span>' +
    '<span class="cpb-track"><span class="cpb-fill"></span></span>' +
    '<span class="cpb-count"></span>' +
    '<span class="cpb-pct"></span>' +
    '<span class="cpb-streak" style="display:none"></span>' +
    (isHome ? '' : '<span class="cpb-cta">' + cta + ' &#8594;</span>');
  document.body.appendChild(bar);
  document.body.style.paddingBottom = "56px";
  paintCourseBar();
}
function paintCourseBar() {
  const bar = document.getElementById("course-progress-bar");
  if (!bar) return;
  const s = CourseSync.stats();
  bar.querySelector(".cpb-fill").style.width = s.pct + "%";
  bar.querySelector(".cpb-count").textContent = s.done + "/" + s.total;
  bar.querySelector(".cpb-pct").textContent = s.pct + "%";
  const streak = bar.querySelector(".cpb-streak");
  if (s.streak > 0) { streak.style.display = ""; streak.textContent = "\u{1F525} " + s.streak; }
  else streak.style.display = "none";
}
CourseSync.onChange(paintCourseBar);

if (document.readyState !== "loading") { wireLessonButtons(); injectCourseBar(); }
else document.addEventListener("DOMContentLoaded", () => { wireLessonButtons(); injectCourseBar(); });
initFirebase();
