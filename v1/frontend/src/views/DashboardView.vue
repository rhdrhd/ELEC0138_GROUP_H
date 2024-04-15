<script setup>
import router from '@/router';
import { ref, onMounted } from 'vue'
const isDebug = ref(false)

const backend_url = import.meta.env.VITE_APP_BACKEND_URL
const dashboard_api = backend_url + '/api/v1/dashboard'
const app_mode = import.meta.env.VITE_APP_MODE

const token = ref('')
const resp = ref(null)
const username = ref('')
const email = ref('')
const balance = ref('10000.00') // dummy value

async function edit(field) {
  let newValue = prompt(`Enter new ${field}`);
  if (!newValue) {
    return;
  }
  
  try {
    const response = await fetch(`${backend_url}/update_user`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token.value,
      },
      body: JSON.stringify({
        username: username.value,
        field: field,
        new_value: newValue
      }),
      credentials: 'include',
    });

    const data = await response.json();
    if (response.ok) {
      alert(data.msg);
      if (field === 'username') username.value = newValue;
      else if (field === 'email') email.value = newValue;
    } else {
      alert(data.msg);
    }
  } catch (error) {
    console.error('Update Error:', error);
    alert('Failed to update data');
  }
}

async function deleteUser() {
  const confirmDelete = confirm("Are you sure you want to delete your account? This cannot be undone.");
  if (!confirmDelete) {
    return;
  }
  
  try {
    const response = await fetch(`${backend_url}/delete_user`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token.value,
      },
      body: JSON.stringify({ username: username.value }),
      credentials: 'include',
    });

    const data = await response.json();
    if (response.ok) {
      alert(data.msg);
      userLogout();
    } else {
      alert(data.msg);
    }
  } catch (error) {
    console.error('Delete Account Error:', error);
    alert('Failed to delete account');
  }
}


async function userDashboard() {
  console.log('User dashboard')
  if (app_mode == "safe") {
    try {
      token.value = 'Bearer ' + localStorage.getItem('userToken');
      const response = await fetch(dashboard_api, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token.value,
        },
        credentials: 'include',
      });
      const data = await response.json();
      resp.value = data
      console.log(data);
      if (response.ok) {
        console.log("get /api/v1/dashboard response successfully")
        username.value = data.data.user.username
        email.value = data.data.user.email
      } else if (response.status === 401) {
        // Login failed, remove the token if it exists
        localStorage.removeItem('userToken');
        alert(data.msg); // Invalid login
      } else {
        alert(data.msg); // Error
      }
    } catch (error) {
      console.error('Dashboard Page Error:', error);
    }
  } else {
    // TODO (unsafe mode)
    // now the same as safe mode
    console.warn("NotImplementedError: unsafe mode for dashboard API")
    try {
      token.value = 'Bearer ' + localStorage.getItem('userToken');
      const response = await fetch(dashboard_api, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token.value,
        },
        credentials: 'include',
      });
      const data = await response.json();
      resp.value = data
      console.log(data);
      if (response.ok) {
        console.log("get /api/v1/dashboard response successfully")
        username.value = data.data.user.username
      } else if (response.status === 401) {
        // Login failed, remove the token if it exists
        localStorage.removeItem('userToken');
        alert(data.msg); // Invalid login
      } else {
        alert(data.msg); // Error
      }
    } catch (error) {
      console.error('Dashboard Page Error:', error);
    }
  }
}

function userLogout() {
  if (app_mode == "safe") {
    localStorage.removeItem('userToken');
    localStorage.removeItem('isVerified');
    localStorage.removeItem('usernameForVerification');
    localStorage.removeItem('emailForVerification');
    token.value = '';
    alert('User successfully logged out! See you next time!');
    router.push('/login');
  } else {
    // TODO (unsafe mode)
    // now the same as safe mode
    console.warn("NotImplementedError: unsafe mode for userLogout")
    localStorage.removeItem('userToken');
    token.value = '';
    alert('User successfully logged out! See you next time!');
    router.push('/login');
  }
}

onMounted(() => {
  userDashboard();
})
</script>

<template>
  <div class="dashboard-container">
    <h1>Dashboard</h1>
    <div class="info-card">
      <h2>Username</h2>
      <p>{{ username }}</p>
      <button @click="edit('username')">Edit</button>
    </div>
    <div class="info-card">
      <h2>Email</h2>
      <p>{{ email }}</p>
      <button @click="edit('email')">Edit</button>
    </div>
    <div class="info-card">
      <h2>Password</h2>
      <p>••••••••</p>
      <button @click="edit('password')">Edit</button>
    </div>
    <div class="info-card">
      <h2>Balance</h2>
      <p>{{ balance }}</p>
      <button @click="edit('balance')">Edit</button>
    </div>
    <button class="logout-button" @click="userLogout">Sign Out</button>
    <button class="delete-button" @click="deleteUser">Delete Account</button>
  </div>
</template>


<style scoped>
.dashboard-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.info-card {
  background: #f4f4f4;
  padding: 20px;
  margin: 10px 0;
  width: 300px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  text-align: center;
}

button {
  margin-top: 10px;
  padding: 8px 16px;
  font-size: 16px;
  cursor: pointer;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 5px;
}

button:hover {
  background-color: #0056b3;
}

.logout-button {
  padding: 10px 20px;
  background-color: red;
  margin-top: 20px;
}

.delete-button {
  padding: 10px 20px;
  background-color: #dc3545;
  color: white;
  margin-top: 10px;
}

.delete-button:hover {
  background-color: #c82333;
}


</style>
