let otpTimer;
let otpTimeRemaining = 60;

function generateOTP() {
    // 生成6位随机OTP数字
    return Math.floor(100000 + Math.random() * 900000);
}

function startOTPTimer() {
    otpTimer = setInterval(() => {
        otpTimeRemaining--;
        document.getElementById('otpTimer').textContent = `${otpTimeRemaining} 秒后失效`;

        if (otpTimeRemaining === 0) {
            clearInterval(otpTimer);
            document.getElementById('otpInput').value = '';
            document.getElementById('otpInput').disabled = true;
        }
    }, 1000);
}

function refreshOTP() {
    const newOTP = generateOTP();
    document.getElementById('otpInput').value = newOTP;
    document.getElementById('otpInput').disabled = false;
    otpTimeRemaining = 60;
    startOTPTimer();
}

document.getElementById('refreshOTPBtn').addEventListener('click', refreshOTP);

// 初始化OTP
refreshOTP();
