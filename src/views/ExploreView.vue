<template>
    <div class="explore" v-if="renderComponent">
        <div class="explore-left">
             <div class="explore-card" v-for="post in posts">
                <div class="explore-user">
                    <RouterLink  class="link" :to="{path: '/users/' + post.user_id, component: () => ('../views/UserProfileView.vue')}">
                        <img :src="post.profile">
                        <div>{{ post.username }}</div>
                    </RouterLink>
                </div>
                <div class="explore-img">
                    <img :src="post.photo">
                </div>
                <div class="explore-desc">
                    {{ post.caption }}
                </div>
                <div class="explore-stats">
                    <div class="likes"  @click="() => likedPost(post.id)">
                        <img src="heart.png" alt="">
                        <div><span>{{ post.likes }}</span> likes</div>
                    </div>
                    <div id="date">{{ post.created_at.split(" ").splice(1,3).join(" ") }}</div>
                </div>
            </div>

            
        </div>
        <div class="explore-right">
            <RouterLink  class="link" to="/posts/new">New Post</RouterLink>
        </div>
    </div>
</template>
<script setup>
    import {ref, onMounted, nextTick} from 'vue'
    import { RouterLink, useRouter } from "vue-router"
    const token = localStorage.getItem("token")
    const renderComponent = ref(true)

    let posts= ref([])
    let csrf_token = ref("")
    let result = ref([])

    onMounted(() => {
        fetchPosts().then(data => posts.value = data)
        getCsrfToken()
    })

    const forceRender = async () => {
        renderComponent.value = false;
        await nextTick();
        renderComponent.value = true;
    };

    const fetchPosts = async() => {
        const res = await fetch("/api/v1/posts")
        const {posts} = await res.json()
        const arr = []
        for (let item of posts) {
            const user = await fetchUser(item.user_id)
            const newObj = {
                ...item,
                username: user.username,
                profile: user.profile_photo
            }
            arr.push(newObj)
        }
        return arr
    }

  
    const fetchUser = async(id) => {
        
        const res = await fetch(`/api/v1/users/${id}`)
        const data = await res.json()
        return data
        
    }
    
    const getCsrfToken = () => {
        fetch('/api/v1/csrf-token')
        .then(res => res.json())
        .then(data => {
            csrf_token.value = data.csrf_token
        })
    }

    const likedPost = (id) => {
        fetch(`/api/v1/posts/${id}/like`, {
            method: "POST",
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
        fetchPosts().then(data => posts.value = data)
        forceRender()
    }


</script>
<style>
 .explore {
    display: flex;
    margin-top: 50px;
    height: 100vh;
    width: 100vw;
 }

 .explore-left {
    width: 100%;
    display: flex;
    flex-direction: column;
    flex:3;
    margin: 0 auto;
 }

 .explore-card {
    display: flex;
    flex-direction: column;
    padding: 15px;
    margin-right: auto;
    margin-left: auto;
    width: 700px;
    margin-bottom: 10px;
    gap: 10px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.5);
 }

 .explore-user .link{
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
    font-weight: 500;
    color: rgb(83, 83, 83);
    
 }

 .explore-user img {
    width: 20px;
    border-radius: 50%;
    object-fit: cover;
    
 }

 .explore-img > img {
    width: 100%;
    height: 500px;
    object-fit: contain;
 }

 .explore-desc {
    margin-bottom: 50px;
    color: gray;
 }

 .explore-stats {
    width: 100%;
    display: flex;
    justify-content: space-between;
 }

 .likes {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 500;
 }

 .likes > img {
    width: 15px;
    object-fit: contain;
 }

 .explore-right {
    flex: 1;
    display: flex;
    justify-content: center;
 }

 .explore-right .link {
    text-decoration: none;
    color: #fff;
    background: rgb(36, 154, 184);
    height: 30px;
    width: 200px;
    text-align: center;
    border-radius: 3px;
 }

 #date {
    font-weight: 500;
 }
</style>