import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/blog" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    published: z.coerce.date(),
    updated: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false)
  })
});

const projects = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/projects" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    order: z.number().default(999),
    featured: z.boolean().default(false),
    status: z.string().default("active"),
    tags: z.array(z.string()).default([]),
    links: z
      .array(
        z.object({
          label: z.string(),
          url: z.url()
        })
      )
      .default([])
  })
});

const cv = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/cv" }),
  schema: z.object({
    name: z.string(),
    title: z.string(),
    location: z.string(),
    email: z.email(),
    github: z.string(),
    summary: z.string(),
    experience: z.array(
      z.object({
        role: z.string(),
        organization: z.string(),
        location: z.string(),
        period: z.string(),
        highlights: z.array(z.string()).default([]),
        url: z.url().optional()
      })
    ),
    education: z.array(
      z.object({
        program: z.string(),
        institution: z.string(),
        location: z.string(),
        period: z.string(),
        details: z.array(z.string()).default([]),
        url: z.url().optional()
      })
    ),
    community: z.array(
      z.object({
        role: z.string(),
        organization: z.string(),
        location: z.string(),
        period: z.string(),
        highlights: z.array(z.string()).default([]),
        url: z.url().optional()
      })
    ),
    skills: z.array(
      z.object({
        group: z.string(),
        items: z.array(z.string())
      })
    ),
    achievements: z.array(
      z.object({
        name: z.string(),
        period: z.string(),
        highlights: z.array(z.string()).default([]),
        url: z.url().optional()
      })
    ),
    interests: z.array(
      z.object({
        group: z.string(),
        items: z.array(z.string())
      })
    )
  })
});

export const collections = { blog, projects, cv };
