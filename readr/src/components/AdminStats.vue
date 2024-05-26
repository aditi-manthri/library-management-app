<template>
  <navbar></navbar>
  <h1>Librarian Statistics</h1>
  <div class="chart-container">
    <img :src="piechartUrl" alt="Section Distribution">
    <img :src="barchartUrl" alt="Books Issued">
  </div>  
</template>

<script>
import axios from 'axios';
import Navbar from './AdminNav.vue';

export default {
  components:{
    Navbar
  },

  data(){
    return{
      piechartUrl: null,
      barchartUrl: null,
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

    const barResponse = await axios.get('/adminstats/bar', { responseType: 'blob' });
    console.log(barResponse);  
    const reader2 = new FileReader();
    reader2.onload = () => {
      this.barchartUrl = reader2.result;
      console.log(reader2.result); 
    };
    reader2.readAsDataURL(new Blob([barResponse.data]));
  },
};
</script>

<style scoped>
.chart-container {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}
.chart-container img {
  max-width: 48%;
  max-height: 90vh; 
  object-fit: contain; 
}
</style>