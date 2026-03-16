<template>
  <span class="typewriter-wrap">
    <span>{{ displayed }}</span>
    <span class="cursor" v-if="typing">▌</span>
  </span>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
const props = defineProps({ text: { type: String, default: '' }, speed: { type: Number, default: 35 }, delay: { type: Number, default: 0 } })
const displayed = ref('')
const typing    = ref(false)

function type() {
  displayed.value = ''
  typing.value = true
  let i = 0
  const interval = setInterval(() => {
    displayed.value += props.text[i]
    i++
    if (i >= props.text.length) { clearInterval(interval); typing.value = false }
  }, props.speed)
}

onMounted(() => setTimeout(type, props.delay))
watch(() => props.text, () => setTimeout(type, props.delay))
</script>

<style scoped>
.typewriter-wrap { display:inline; }
.cursor { color:#c9a227; animation:blink-cursor 0.8s step-end infinite; }
</style>
