<script setup>
import router from '@/router';
import { ref, onMounted } from 'vue'

const backend_url = import.meta.env.VITE_APP_BACKEND_URL
const dashboard_api = backend_url + '/api/v1/dashboard'

const token = ref('')
const resp = ref(null)
const username = ref('')

async function userDashboard() {
  console.log('User dashboard')
  try {
    token.value = 'Bearer ' + localStorage.getItem('userToken');
    const response = await fetch(dashboard_api, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token.value,
      },
    });
    const data = await response.json();
    resp.value = data
    console.log(data);
    if (response.ok) {
      console.log("get /api/v1/dashboard response successfully")
      username.value = data.data.user.username
    } else if (response.status === 401) {
      localStorage.removeItem('userToken');
      alert(data.msg); // Invalid login
    } else {
      alert(data.msg); // Error
    }
  } catch (error) {
    console.error('Dashboard Page Error:', error);
  }
}

function userLogout() {
  localStorage.removeItem('userToken');
  token.value = '';
  alert('User successfully logged out! See you next time!');
  router.push('/login');
}

onMounted(() => {
  userDashboard();
})
</script>


<template>
  <h1>Dashboard</h1>
  <div>
    <button @click="userLogout">
      Sign Out
    </button>
  </div>
</template>
