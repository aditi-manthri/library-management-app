<template>
    <nav>
        <a> Dear Readr</a>
    </nav>
    <div class="container">
        <h1>Sign Up</h1>
        <form @submit.prevent="signup">
            <input class='input-field'  placeholder="Username" type="text" id="username" v-model="username" required /><br><br>
            <input class='input-field'  placeholder="Password" type="password" id="password" v-model="password" required /><br><br>
            <input class='input-field'  placeholder="Email" type="text" id="email" v-model="email" required /><br><br>
            <button class="buttons" type="submit">Sign Up</button><br><br>
        </form>
        <router-link to="/login">
            <button class="buttons">Go to Login</button>
        </router-link><br><br>
        <p>{{ errorMessage }}</p>
    </div>
  </template>

<script>
import axios from 'axios';

export default{
    data(){
        return{
            username:'',
            password:'',
            role:'user',
            email: '',
            errorMessage: '',
        };
    },

    methods: {
        
            async signup(){
                try {
                    const response = await axios.post('http://127.0.0.1:8000/signup',{
                            username: this.username,
                            password: this.password,
                            role: this.role,
                            email: this.email,
                        });
                        console.log('Singup Succesful',response.data);
                        this.$router.push("/login");
                    } catch(error){
                        console.error(error.response.data);
                        this.errorMessage = "Could Not Create Account."
                    }
            }
}
}
</script>