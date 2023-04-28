<template>
    <div class="profile-container">
        <div class="profile-card">
            <div class="profile-photo">
                <img :src="user.profile_photo">
            </div>
            <div class="profile-desc">
                <h3>{{ user.firstname }} {{ user.lastname }}</h3>
                <span>{{ user.location }}</span>
                <span>Member since <span> Apr 2023</span></span>
                <p>{{ user.biography }}</p>
            </div>
            <div class="profile-stats">
                <div class="sub">
                    <div class="stat"><span>{{ posts.length }}</span>posts</div>
                    <div class="stat"><span>{{followers.followers}}</span>followers</div>
                </div>
                <a href="#" class="follow-link" v-if="id!='currentuser'" @click="() => followUser(id)">{{ text }}</a>
            </div>
        </div>
        
        <div class="profile-gallery">
            <div class="img-container" v-for="post in posts">
                <img :src="post.photo">
            </div>
            
        </div>
    </div>
</template>
<script setup>
    import {ref, onMounted, onUpdated} from 'vue'
    import {useRoute} from 'vue-router'
    let csrf_token = ref("")

    const followBtn = document.getElementById("follow")

    const user = ref({})
    // let userId = ref(0)
    const posts = ref([])
    const followers = ref(0)
    const token = localStorage.getItem("token")
    const text = ref("follow")
    const route = useRoute()
    let id = route.params.id
    console.log(id)

    onMounted(() => {
        fetchUser(id).then(data => {
            user.value = data
            console.log(data)
        })
        fetchPosts(id).then(data => posts.value = data.posts)
        getFollowers(id).then(data => followers.value = data)
        getCsrfToken()
    })

    const getCsrfToken = () => {
        fetch('/api/v1/csrf-token')
        .then(res => res.json())
        .then(data => {
            csrf_token.value = data.csrf_token
        })
    }


    const fetchUser = async(id) => {
        const res = await fetch(`/api/v1/users/${id}`, {
            method: "GET",
            headers: {
                'Authorization': "Bearer " + token
            }
        })
        const data = await res.json()
        return data
    }

    const getFollowers = async(id) => {
        ///api/users/<userId>/follow
            const user = await fetchUser(id)
            id = user.id
            const res = await fetch(`/api/users/${id}/follow`, {
            method: "GET",
            headers: {
                'Authorization': "Bearer " + token
            }
        })
        const data = await res.json()
        return data
    }

    const followUser = async(id) => {
        const targetUserId = id
        const currentUser = await fetchUser("currentuser")
        // console.log(targetUserId, currentUser.id)
        const res = await fetch(`/api/users/${currentUser.id}/follow`, {
            method:"POST",
            body: JSON.stringify({"follow_id": targetUserId}),
            headers: {
                'X-CSRFToken': csrf_token.value,
                'Authorization': "Bearer " + token,
                'Content-Type': "application/json"
            }
        })
        const data = await res.json()
       
        text.value = "following"
    
        console.log(data)

    }

    const fetchPosts = async(id) => {
        const user = await fetchUser(id)
        id = user.id
        const res = await fetch(`/api/v1/users/${id}/posts`, {
            method: "GET",
            headers: {
                'Authorization': "Bearer " + token
            }
        })
        const data = await res.json()
        return data
    }
</script>
<style>
    .profile-container {
        height: 100vh;
        width: 100vw;
        margin-top: 50px;
    }

    .profile-card {
        width: 90%;
        /* background: rgb(226, 200, 200); */
        height: 200px;
        display: flex;
        margin: 20px auto;
        gap: 20px;
        align-items: center;
        box-shadow: 2px 2px 5px rgba(0,0,0, 0.5);
    }

    .profile-photo {
        width: 180px;
        height: 180px;
        border-radius: 50%;
        overflow: hidden;
        margin-left: 30px;
    }

    .profile-desc {
        display: flex;
        flex-direction: column;
        flex: 3;
    }

    .profile-desc > span {
        color: gray;
    }

    .profile-desc > p {
        color: gray;
        margin-top: 20px;
    }

    .profile-stats {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
        flex: 1;
    }

    .profile-stats .sub {
        display: flex;
        justify-content: space-around;
        text-align: center;
        gap: 20px;
    }

    .profile-stats .stat {
        display: flex;
        flex-direction: column;
    }

    .profile-stats .stat {
        color: gray;
    }

    .profile-stats .stat span {
        color: #000;
        font-weight: 700;
        font-size: 30px;
    }

    .profile-photo > img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .follow-link {
        color: #fff;
        background: #32a4c7;
        text-decoration: none;
        width: 200px;
        text-align: center;
        border-radius: 2px;
        margin-right: 10px;
        padding: 5px;
    }

    .profile-gallery {
        width: 100%;
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin: 0 auto;
        justify-content: center;
    }

    .profile-gallery > .img-container {
        width: 30%;
        overflow: hidden;
        display: flex;
        justify-content: center;
    }
    .profile-gallery img {
        width: 300px;
        height: 300px;
    }
</style>