
const baseUrl = "http://localhost:5001"

async function sendFormData(url, formData, multipart= false) {
    const plainFormData = Object.fromEntries(formData.entries());
    const formDataJsonString = JSON.stringify(plainFormData);

    const fetchConfig= {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: formDataJsonString
    }

    if (multipart) {
        delete fetchConfig.headers["Content-Type"]
        fetchConfig.body = formData
    }

    console.log(fetchConfig)

    const response = await fetch(baseUrl + url, fetchConfig);

    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return response
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
    const res = await sendFormData('/certificate', formData)
    const blob = await res.blob()
    const fileUrl = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = fileUrl;
    a.download = 'certificate.pem';
    a.click();
    a.remove()
    return Promise.resolve()
}

async function login(formData) {
    const res = await sendFormData('/login', formData, true)
    // const data = await res.json()
    // localStorage.setItem('token', data.access_token)
}