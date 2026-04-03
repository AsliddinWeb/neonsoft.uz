<script setup lang="ts">
import HeroSection from '@/components/public/HeroSection.vue'
import AboutSection from '@/components/public/AboutSection.vue'
import ServicesSection from '@/components/public/ServicesSection.vue'
import ProjectsSection from '@/components/public/ProjectsSection.vue'
import TeamSection from '@/components/public/TeamSection.vue'
import BlogSection from '@/components/public/BlogSection.vue'
import PartnersSection from '@/components/public/PartnersSection.vue'
import ContactSection from '@/components/public/ContactSection.vue'
import CtaBand from '@/components/public/CtaBand.vue'
import { useSeo } from '@/composables/useSeo'

useSeo({ title: 'Bosh sahifa' })
</script>

<template>
  <div>
    <HeroSection />
    <AboutSection />
    <ServicesSection />
    <ProjectsSection />
    <TeamSection />
    <BlogSection />
    <PartnersSection />
    <ContactSection />
    <CtaBand />
  </div>
</template>
