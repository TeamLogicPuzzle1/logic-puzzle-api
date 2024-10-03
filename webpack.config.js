const path = require('path');
const fs = require('fs');

module.exports = {
    entry: './index.js', // 진입 파일
    output: {
        filename: 'bundle.js', // 출력 파일 이름
        path: path.resolve(__dirname, 'dist'), // 출력 디렉토리
    },
    module: {
        rules: [
            {
                test: /\.js$/, // .js 파일에 대한 규칙
                exclude: /node_modules/, // node_modules 제외
                use: {
                    loader: 'babel-loader', // Babel 사용
                },
            },
        ],
    },
    resolve: {
        extensions: ['.js'], // 사용할 파일 확장자
    },
    devServer: {
        static: {
            directory: path.join(__dirname, 'public'), // 정적 파일 제공할 디렉토리
        },
        port: 8082, // 서버 포트
        server: 'https', // HTTPS 서버 사용
        https: {
            key: fs.readFileSync(path.join(__dirname, 'ssl', 'server.key')), // SSL 키 파일
            cert: fs.readFileSync(path.join(__dirname, 'ssl', 'server.cert')), // SSL 인증서 파일
        },


open: true, // 서버 시작 시 브라우저 열기
        hot: true, // 핫 모듈 교체 활성화
    },
    mode: 'development', // 모드 설정
};