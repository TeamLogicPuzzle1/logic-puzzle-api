// Import the functions you need from the Firebase SDKs
import { initializeApp } from 'firebase/app';
import { getMessaging, onBackgroundMessage } from 'firebase/messaging';

// Firebase 초기화
const firebaseConfig = {
    apiKey: "AIzaSyD2fiBYZHuV2r9XhxVbhykd6ox8EViIK2c",
    authDomain: "alarm1-a8149.firebaseapp.com", // 이 값을 확인 후 수정하세요
    projectId: "alarm1-a8149",
    storageBucket: "alarm1-a8149.appspot.com",
    messagingSenderId: "101045129713",
    appId: "1:101045129713:web:437bca668ff9731cb23450",
    vapidKey: "BBeOd-BKgpP-pgxUusTsNVIBiu7zJGZ0PC4AulRuCNLFUGSMhVH48G8Lpx63KzpCNHpyaDheGplegKVLhju2Kkk"
};

// Firebase 앱 초기화
initializeApp(firebaseConfig);
const messaging = getMessaging();

// 백그라운드 메시지 처리
onBackgroundMessage(messaging, (payload) => {
    console.log('Received background message: ', payload);
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: '/firebase-logo.png' // 원하는 아이콘 경로를 설정하세요.
    };

    // 알림 표시
    self.registration.showNotification(notificationTitle, notificationOptions);
});