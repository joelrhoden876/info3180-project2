<template>
    <div class="post">
    <h1>New Post</h1>
    <form @submit.prevent="saveMovie" id="postForm">
        <div v-if="result.errors">
            <ul class="alert alert-danger">
                <li v-for="error in result.errors">{{ error }}</li>
            </ul>
        </div>
        <div v-if="result.message">
            <div class="alert alert-success">{{ result.message }}</div>
        </div>
        <div class="form-group">
            <label for="caption" class="form-label">caption</label>
            <textarea row="10" name="caption" class="form-control" />
        </div>
        <div class="form-group">
            <label for="photo" class="form-label">Photo</label>
            <input type="file" name="photo" class="form-control-file">
        </div>
        <input type="submit">
    </form>
</div>
</template>

<script setup>

    import {ref, onMounted} from 'vue'
    const token = localStorage.getItem("token")
    let csrf_token = ref("")
    let result = ref([])
    // const user = ref({})

    const getCsrfToken = () => {
        fetch('/api/v1/csrf-token')
        .then(res => res.json())
        .then(data => {
            csrf_token.value = data.csrf_token
        })
    }

    onMounted(() => {
        getCsrfToken()
    })

    const fetchUser = async() => {
        const res = await fetch("/api/v1/users/currentuser", {
            method: "GET",
            headers: {
                'Authorization': "Bearer " + token
            }
        })
        const data = await res.json()
        return data
    }

    const saveMovie = async() => {
        let user = await fetchUser()
        let postForm = document.getElementById("postForm")
        let form_data = new FormData(postForm)
        
        // console.log(...form_data.entries())
        fetch(`/api/v1/users/${user.id}/posts`, {
            method: "POST",
            body: form_data,
            headers: {
                'X-CSRFToken': csrf_token.value,
                'Authorization': "Bearer " + token
            }
        })
        .then(res => res.json())
        .then(data => {
            result.value = data
            console.log(data)
        })
        .catch(err => result.value = err)
    }

</script>

<style>
.post {
    padding: 20px;
    box-shadow: 2px 2px 5px rgba(0, 0,0,0.5);
}
    form {
        display: flex;
        flex-direction: column;
    }
    .form-group {
        display: flex;
        flex-direction: column;
        margin: 10px 0;
    }

    .form-group > label {
        font-weight: bold;
    }

    input[type="submit"] {
        margin-top: 20px;
        width: 100px;
        border: none;
        background: rgb(76, 120, 240);
        border-radius: 5%;
        color: #fff;
    }

    input[type="submit"]:hover {
        cursor: pointer;
        background: rgb(6, 24, 104);
    }

    .alert {
        padding-left: 50px;
    }

</style>