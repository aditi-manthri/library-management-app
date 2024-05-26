<template>
  <nav class="newnav">
       <div class="name">
        <router-link  style="text-decoration: none; color: inherit;" to="/dashboard">Reader Dashboard</router-link>
       </div>
       <div>
       <router-link  style="text-decoration: none; color: inherit;" to="/stats">Stats</router-link> |
       <router-link  style="text-decoration: none; color: inherit;" to="/mybooks">My Books</router-link> |
       <router-link  style="text-decoration: none; color: inherit;" to="/search">Search</router-link> |
       <router-link  style="text-decoration: none; color: inherit;" to="/login">Logout</router-link>
       </div>  
   </nav>
</template>

<style scoped>
  .search-container {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }  
</style>