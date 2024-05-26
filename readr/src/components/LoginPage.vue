<template>
     <nav>
        <a> Dear Readr</a>
    </nav>
    <div class="container">
        <h1>Login</h1>
        <form @submit.prevent="login">
            <input class='input-field' placeholder="Username" type="text" id="username" v-model="username" required /><br><br>
            <input class='input-field'  placeholder="Password" type="password" id="password" v-model="password" required /><br><br>
            <button class="buttons" type="submit">Login</button><br><br>
        </form>
        <router-link to="/signup">
            <button class="buttons">Go to Sign Up</button>
        </router-link>
        <p>{{ errorMessage }}</p>
    </div>
  </template>
  
  
  <script>
  import axios from 'axios';
  
  export default{
    data(){
        return{
            isLogin: true,
            username: '',
            password: '',
            errorMessage: '',
        };
    },
    methods:{
        async login(){
            try{
                const response = await axios.post('http://127.0.0.1:8000/login',{
                    username: this.username,
                    password: this.password
                });
  
                localStorage.setItem('access_token',response.data.access_token);
                localStorage.setItem('userRole',response.data.userRole);
                localStorage.setItem('user_id',response.data.user_id);
                localStorage.setItem('isauthenticated', true);
                if (response.data.userRole === 'user') {
                  this.$router.push('/dashboard');
                } else if (response.data.userRole === 'admin') {
                  this.$router.push('/admindashboard');
                } 
              }
                catch(error){
                console.error(error.message)
                this.errorMessage = "Incorrect Username and/or Password."
            }
        },
    },
  }
  </script>