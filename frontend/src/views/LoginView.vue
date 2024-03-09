<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const backend_url = import.meta.env.VITE_APP_BACKEND_URL
const login_api = backend_url + '/login'

const username = ref('')
const password = ref('')
const token = ref('')
const isDebug = ref(false)
const resp = ref(null)

async function userLogin() {
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
    console.error('Error:', error);
  }
}
</script>

<template>
  <h1>Login</h1>
  <div>
    <li>Username: <input v-model="username"></li>
    <li>Password: <input v-model="password"></li>
    <button @click.prevent="userLogin">
      Submit
    </button>
  </div>
  <div>
    <button @click.prevent="isDebug = !isDebug">
      Debug Mode
    </button> isDebug: {{ isDebug }}
    <div v-if="isDebug">
      Debug info:
      <li>username: {{ username }}</li>
      <li>password: {{ password }}</li>
      <li>response: {{ resp }}</li>
      <li>token: {{ token }}</li>
    </div>
  </div>
</template>

<style>
h1 {
  margin-bottom: 2rem; /* Increase space below the heading */
  line-height: 1.4; /* Adjust line height to increase space between lines of text */
}

li {
  margin: 1rem 0; /* Add top and bottom margin to list items */
  line-height: 1.6; /* Increase line height for more space between lines */
  list-style-type:none;
}

input {
  margin: 0.5rem 0; /* Add some space above and below input fields */
  padding: 0.5rem; /* Add padding inside input fields for better visual and typing experience */
  border: 1px solid #ccc; /* Optional: adds a border to make inputs more defined */
  border-radius: 4px; /* Optional: rounds the corners of the input fields */
}

button {
  margin-top: 1rem; /* Adds space above the button */
  /* Include previous button styles here */
}

/* Previous button styles for a better look */
button {
  background-color: #81D8D0;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

button:hover {
  background-color: #81D8D0;
  transform: scale(1.05);
}

button:active {
  background-color: #eaedf1;
  transform: scale(0.95);
}
</style>