<template>
  <span class="glitch-wrap" :data-text="text">
    <span class="glitch-main">{{ text }}</span>
    <span class="glitch-layer a" aria-hidden="true">{{ text }}</span>
    <span class="glitch-layer b" aria-hidden="true">{{ text }}</span>
  </span>
</template>

<script setup>
defineProps({ text: { type: String, default: '' } })
</script>

<style scoped>
.glitch-wrap { position:relative; display:inline-block; }
.glitch-main { position:relative; z-index:1; }
.glitch-layer { position:absolute; top:0; left:0; width:100%; }
.glitch-layer.a { color:#ff0040; animation:glitch-1 4s infinite linear; opacity:0.6; }
.glitch-layer.b { color:#00ffff; animation:glitch-2 4s infinite linear 0.5s; opacity:0.6; }
</style>
