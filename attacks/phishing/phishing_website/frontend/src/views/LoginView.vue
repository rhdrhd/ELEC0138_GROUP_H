<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const backend_url = import.meta.env.VITE_APP_BACKEND_URL
const login_api = backend_url + '/api/v1/login'

const username = ref('')
const password = ref('')
const token = ref('')

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
    if (response.ok) {
      token.value = data.data.token
      localStorage.setItem('userToken', token.value);
      router.push('/dashboard')
    } else {
      alert(data.msg); // Error or invalid login
    }
  } catch (error) {
    localStorage.removeItem('userToken');
    console.error('Login failed:', error);
  }
}

onMounted(() => {
  if (localStorage.getItem('userToken') !== "") {
    router.push('/dashboard')
  }
})
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