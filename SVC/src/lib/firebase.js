import firebase from 'firebase/app';
import 'firebase/firestore';
import 'firebase/auth';
import 'firebase/storage'



// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDUQjhTlgpOqYxh2Aqe8qMHk4Zon3DgbfU",
  authDomain: "edusphere-e7257.firebaseapp.com",
  projectId: "edusphere-e7257",
  storageBucket: "edusphere-e7257.appspot.com",
  messagingSenderId: "383491292694",
  appId: "1:383491292694:web:51bf24d8bb6b1f1153bf37",
  measurementId: "G-PETXF5DCC5"
};

firebase.initializeApp(firebaseConfig);

const db = firebase.firestore();
const auth = firebase.auth()
const provider = new firebase.auth.GoogleAuthProvider();
const storage = firebase.storage()

export { auth, provider, storage }
export default db;
