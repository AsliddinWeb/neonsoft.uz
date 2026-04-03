export interface User {
  id: number
  email: string
  full_name: string
  role: 'superadmin' | 'admin'
  is_active: boolean
  created_at: string
}

export interface Service {
  id: number
  title: string
  slug: string
  short_description: string
  description: string
  icon: string | null
  order: number
  is_active: boolean
  created_at: string
}

export interface Project {
  id: number
  title: string
  slug: string
  description: string
  client_name: string | null
  tech_stack: string[] | null
  image_url: string | null
  project_url: string | null
  github_url: string | null
  is_featured: boolean
  order: number
  is_active: boolean
  completed_at: string | null
  created_at: string
}

export interface TeamMember {
  id: number
  full_name: string
  position: string
  bio: string | null
  photo_url: string | null
  linkedin_url: string | null
  github_url: string | null
  telegram_url: string | null
  order: number
  is_active: boolean
  created_at: string
}

export interface BlogPost {
  id: number
  title: string
  slug: string
  excerpt: string | null
  content: string
  cover_image_url: string | null
  tags: string[] | null
  is_published: boolean
  views: number
  author: User
  published_at: string | null
  created_at: string
  updated_at: string | null
}

export interface ContactMessage {
  id: number
  full_name: string
  email: string | null
  phone: string | null
  subject: string | null
  message: string
  source: string
  is_read: boolean
  created_at: string
}

export interface SiteSetting {
  id: number
  company_name: string
  tagline: string | null
  description: string | null
  email: string | null
  phone: string | null
  address: string | null
  logo_url: string | null
  telegram: string | null
  instagram: string | null
  linkedin: string | null
  github: string | null
  meta_title: string | null
  meta_description: string | null
  meta_keywords: string | null
  updated_at: string | null
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}
