<template>
  <router-view/>
</template>

<style>
#app {
  font-family: 'Garamond', serif;
  font-size: 24px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 1px;
  background-color:aquamarine;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}
.newnav{
  display: flex;
  justify-content: space-between;
  padding: 1px;
  background-color: aquamarine;
  padding-left: 20px;
  padding-right: 20px;
}
.container {
  border: none;
  padding: 15px 32px;
  padding-left: 40px;

  font-size: 24px;
  margin: 6px 2px;
  cursor: pointer;
  border-radius: 4px;
}
.input-field {
  flex-grow: 1;
  margin-right: 10px;
  width: 100%;
  font-family: inherit;
  font-size: 24px;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
  border: 2px solid #ccc;
  border-radius: 4px;
}
.buttons {
  font-family: 'Garamond', serif;
  background-color:aquamarine; 
  border: none;
  padding: 15px 32px;
  text-align: center;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 4px;
  text-decoration: none;
  color: #2c3e50;
}
.wbuttons {
  font-family: 'Garamond', serif;
  color: #2c3e50;
  background-color:white; 
  border: none;
  padding: 15px 32px;
  text-align: center;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 4px;
}
.section-container {
   display: flex;
   flex-wrap: wrap;
   justify-content: center;
   }

.section-card {
   flex: 0 0 calc(25% - 10px);
   margin: 10px;
   padding: 20px;
   border: 1px solid #ccc;
   border-radius: 5px;
   background-color: aquamarine;
   box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
   }
.tabl{
  margin-left: auto;
  margin-right: auto;
  font-size: 20px;
}   
.tabl td, .tabl th {
    border: 1px solid #ddd;
    padding: 8px;
  }

.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.search-bar {
  height: 50px;
  width: 250px;
}  
</style>

<script>
export default {
  name: 'App'
}
</script>
