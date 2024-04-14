<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const backend_url = import.meta.env.VITE_APP_BACKEND_URL;
const login_api = `${backend_url}/api/v1/login`;
const app_mode = import.meta.env.VITE_APP_MODE;

const username = ref('');
const password = ref('');
const token = ref('');
const isDebug = ref(false);
const resp = ref(null);
const recaptchaToken = ref(null);  // Store the reCAPTCHA token here
const recaptchaId = ref(null);

const loadRecaptcha = () => {
  if (window.grecaptcha && window.grecaptcha.render) {
    if (recaptchaId.value === null) {
      recaptchaId.value = grecaptcha.render('recaptcha-element', {
        'sitekey': '6Lczk7kpAAAAANd46AiA8tL82izCtQy2MvUA5Oug', // replace with your actual site key
        'callback': (token) => { recaptchaToken.value = token; }  // Store the token, don't login immediately
      });
    }
  } else {
    console.error('reCAPTCHA library not loaded.');
  }
}

const sendLoginCode = async (email) => {
      try {
        await fetch(`${import.meta.env.VITE_APP_BACKEND_URL}/api/v1/send-login-code`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: email }),
        });
      } catch (error) {
        console.error('Error sending login code:', error);
      }
    };

async function userLogin() {
  if (app_mode == "safe"){
    if (!recaptchaToken.value) {
      alert("Please complete the reCAPTCHA to login.");
      return;
    }
    try {
      const response = await fetch(login_api, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          username: username.value,
          password: password.value,
          'g-recaptcha-response': recaptchaToken.value
        }),
      });
      const data = await response.json();
      resp.value = data;
      if (response.ok) {
        token.value = data.data.token;
        localStorage.setItem('userToken', token.value);
        // router.push('/dashboard');
        await sendLoginCode(data.data.email); // Send login code
        localStorage.setItem('emailForVerification', data.data.email); // may have problem if stored in localStorage
        router.push('/verify-code');
      } else {
        alert(data.msg); // Error or invalid login
      }
    } catch (error) {
      console.error('Login failed:', error);
      alert('Login request failed. Please try again later.');
    }
  }
  else{
    // TODO (unsafe mode)
    try {
      const response = await fetch(login_api, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username.value,
          password: password.value,
        }),
        credentials: 'include',
      });
      const data = await response.json();
      resp.value = data
      console.log(data);
      if (response.ok) {
        token.value = data.data.token
        // We can get it by localStorage.getItem('userToken');
        localStorage.setItem('userToken', token.value);
        // navigate to dashboard after login
        router.push('/dashboard')
      } else {
        alert(data.msg); // Error or invalid login
      }
    } catch (error) {
      // Login failed, remove the token if it exists
      localStorage.removeItem('userToken');
      console.error('Login failed:', error);
    }

    console.warn("NotImplementedError: unsafe mode for userLogin")
  }
}

onMounted(() => {
  if (app_mode === "safe" && localStorage.getItem('userToken') !== null) {
    router.push('/dashboard');
  }
  loadRecaptcha();
});

onUnmounted(() => {
  if (recaptchaId.value !== null) {
    grecaptcha.reset(recaptchaId.value);
    recaptchaId.value = null;
  }
});
</script>

<template>
  <h1>Login</h1>
  <div>
    <input v-model="username" type="text" placeholder="Username">
    <input v-model="password" type="password" placeholder="Password">
    <div id="recaptcha-element"></div>
    <button @click.prevent="userLogin"class="login-button">Login</button>
  </div>
  <div>
    <button @click.prevent="isDebug = !isDebug" class="login-button">Toggle Debug</button>
    <div v-if="isDebug">
      Debug Info:
      <ul>
        <li>Username: {{ username }}</li>
        <li>Password: {{ password }}</li>
        <li>Response: {{ resp }}</li>
        <li>Token: {{ token }}</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
@import "@/assets/login.css";
</style>
