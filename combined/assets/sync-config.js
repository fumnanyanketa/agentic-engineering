// ---------------------------------------------------------------------------
// Firebase config for cross-device progress sync.
//
// HOW TO FILL THIS IN (one time):
//   1. Go to https://console.firebase.google.com and create a free project.
//   2. Add a "Web app" to it; Firebase shows you a config object.
//   3. Copy those values into the object below (replace every REPLACE_ME).
//   4. In the console: Build > Authentication > enable "Google" sign-in.
//   5. In the console: Build > Firestore Database > create it (production mode),
//      then paste the security rules from FIREBASE_SETUP.md.
//   6. Authentication > Settings > Authorized domains: add your GitHub Pages
//      domain (for example  yourname.github.io ). localhost is already allowed.
//
// Until you fill this in, the tracker still works, but only in this one browser
// (no cross-device sync, no sign-in). Nothing here is secret: a Firebase web
// config is meant to live in client code. Your data is protected by the
// Firestore security rules, not by hiding these values.
// ---------------------------------------------------------------------------
export const firebaseConfig = {
  apiKey: "REPLACE_ME",
  authDomain: "REPLACE_ME.firebaseapp.com",
  projectId: "REPLACE_ME",
  appId: "REPLACE_ME"
};
