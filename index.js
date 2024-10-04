// Firebase SDK에서 필요한 함수 가져오기
import { initializeApp } from 'firebase/app';
import { getMessaging, onBackgroundMessage } from 'firebase/messaging';

// Firebase 구성
const firebaseConfig = {


apiKey: "AIzaSyD2fiBYZHuV2r9XhxVbhykd6ox8EViIK2c",
    authDomain: "alarm1-a8149.firebaseapp.com",
    projectId: "alarm1-a8149",
    storageBucket: "alarm1-a8149.appspot.com",
    messagingSenderId: "101045129713",


appId: "1:101045129713:web:437bca668ff9731cb23450",
    vapidKey: "BBeOd-BKgpP-pgxUusTsNVIBiu7zJGZ0PC4AulRuCNLFUGSMhVH48G8Lpx63KzpCNHpyaDheGplegKVLhju2Kkk"
};

// Firebase 초기화
const app = initializeApp(firebaseConfig);
const messaging = getMessaging(app);

// 서비스 워커 등록
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/firebase-messaging-sw.js')
        .then((registration) => {
            console.log('Service Worker registered with scope:', registration.scope);
        })
        .catch((error) => {
            console.error('Service Worker registration failed:', error);
            alert('Service Worker registration failed: ' + error);
        });
}

// 백그라운드 메시지 핸들러
onBackgroundMessage(messaging, (payload) => {
    console.log('Received background message: ', payload);
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: '/firebase-logo.png' // 원하는 아이콘 경로 설정
    };

    // 알림 표시
    if (Notification.permission === 'granted') {
        self.registration.showNotification(notificationTitle, notificationOptions);
    }
});