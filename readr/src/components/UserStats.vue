<template>
    <div>
        <navbar></navbar>
        <h1>Book Statistics</h1>
        <img :src="piechartUrl" alt="Book Section Distribution">
    </div>
</template>

<script>
import axios from 'axios';
import Navbar from './UserNav.vue';

export default {
    components:{
        Navbar
    },
    data(){
        return{
        piechartUrl: null,
        };
    },

    async created() {
        const pieResponse = await axios.get('/adminstats/pie', { responseType: 'blob' });
        console.log(pieResponse);
        const reader1 = new FileReader();
        reader1.onload = () => {
        this.piechartUrl = reader1.result;
        console.log(reader1.result); 
        };
        reader1.readAsDataURL(new Blob([pieResponse.data]));
    }
  }
</script>
