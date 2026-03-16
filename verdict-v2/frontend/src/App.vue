<template>
  <RouterView v-slot="{ Component }">
    <Transition name="fade" mode="out-in">
      <component :is="Component" :key="$route.path" />
    </Transition>
  </RouterView>
</template>

<style>
@keyframes glitch-1 {
  0%,100%{clip-path:inset(0 0 98% 0);transform:translateX(-4px)}
  20%{clip-path:inset(20% 0 60% 0);transform:translateX(4px)}
  40%{clip-path:inset(50% 0 30% 0);transform:translateX(-2px)}
  60%{clip-path:inset(80% 0 5% 0);transform:translateX(2px)}
}
@keyframes glitch-2 {
  0%,100%{clip-path:inset(60% 0 20% 0);transform:translateX(4px)}
  25%{clip-path:inset(10% 0 75% 0);transform:translateX(-4px)}
  75%{clip-path:inset(40% 0 40% 0);transform:translateX(2px)}
}
@keyframes typewriter { from{width:0} to{width:100%} }
@keyframes blink-cursor { 0%,100%{border-color:transparent}50%{border-color:#c9a227} }
@keyframes scanline { 0%{top:-5%}100%{top:105%} }
@keyframes redact-reveal { 0%{background:#000;color:transparent}100%{background:transparent;color:inherit} }
@keyframes flicker { 0%,100%{opacity:1}92%{opacity:1}93%{opacity:0.4}94%{opacity:1}96%{opacity:0.7}97%{opacity:1} }
@keyframes fadeUp { from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)} }
@keyframes pulse-gold { 0%,100%{box-shadow:0 0 0 0 rgba(201,162,39,0)} 50%{box-shadow:0 0 12px 4px rgba(201,162,39,0.25)} }
.fade-enter-active,.fade-leave-active{transition:opacity 0.4s ease}
.fade-enter-from,.fade-leave-to{opacity:0}
.noise-layer {
  position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
  opacity:0.5;
}
.scanline-layer {
  position:fixed;left:0;right:0;height:3px;pointer-events:none;z-index:1;
  background:rgba(201,162,39,0.04);animation:scanline 8s linear infinite;
}
</style>
