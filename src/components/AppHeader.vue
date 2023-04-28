<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <img class="icon" src="camera.png" alt="">
        <a class="navbar-brand" href="/">Photogram</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link active">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/explore">Explore</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/users/currentuser">My Profile</RouterLink>
            </li>
            <li v-if="!token" class="nav-item">
              <RouterLink class="nav-link" to="/login">Login</RouterLink>
            </li>
            <li v-else class="nav-item">
              <RouterLink class="nav-link" to="/logout" @click="logout">Logout</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink, useRouter } from "vue-router";
const router = useRouter()
//auth token present or not
const token = localStorage.getItem("token")
console.log(token)

const logout = () => {
  localStorage.removeItem("token")
  window.location.reload()
}

</script>

<style>
/* Add any component specific styles here */
 .icon {
  width: 20px;
}

/*.container-fluid {
  display: flex;
  justify-content: space-between;
  align-items: center;
} */

</style>