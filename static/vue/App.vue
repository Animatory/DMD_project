<template>
  <div class="container">
    <h1>Hello World!</h1>
    <QueryComponent v-for="i in queries" :query='i' :key='i'></QueryComponent>
  </div>
</template>

<script>
import QueryComponent from './QueryComponent.vue'

export default {
    components: {
        QueryComponent
    },
    data: function() {
        return {
            queries: [1, 2, 3, 4, 5, 6, 7, 8]
        }
    }
}
</script>
