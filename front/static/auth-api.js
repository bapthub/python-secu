
const baseUrl = "http://localhost:5000"

async function sendFormData(url, formData) {
    const response = await fetch(baseUrl + url, {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
}
async function signup(formData) {
    await sendFormData('/signup', formData)
}

async function verifyCode(formData) {
    await sendFormData('/code', formData)
}

async function resendCode(formData) {
    await sendFormData('/resend-code', formData)
}

async function getCertificates(formData) {
    await sendFormData('/certificate', formData)
}

async function login(formData) {
    await sendFormData('/login', formData)
}