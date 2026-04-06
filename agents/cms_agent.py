#!/usr/bin/env python3
"""
🗂️ CMS-Agent
Content Management System агент

Создаёт:
- Headless CMS
- Strapi конфигурации
- Contentful интеграции
- Sanitize/validate контент
"""

import argparse
from pathlib import Path
from typing import Dict


class CMSAgent:
    """
    🗂️ CMS-Agent
    
    Специализация: Content Management
    Технологии: Strapi, Contentful, Headless CMS
    """
    
    NAME = "🗂️ CMS-Agent"
    ROLE = "CMS Developer"
    EXPERTISE = ["Strapi", "Contentful", "Headless CMS", "Content Modeling", "API"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["content-types.js"] = """module.exports = {
  // Blog Post Content Type
  'blog-post': {
    kind: 'collectionType',
    collectionName: 'blog_posts',
    info: {
      name: 'Blog Post',
      description: 'Blog articles',
    },
    options: {
      draftAndPublish: true,
    },
    attributes: {
      title: {
        type: 'string',
        required: true,
        maxLength: 255,
      },
      slug: {
        type: 'uid',
        targetField: 'title',
        required: true,
      },
      excerpt: {
        type: 'text',
        maxLength: 500,
      },
      content: {
        type: 'richtext',
        required: true,
      },
      featuredImage: {
        type: 'media',
        multiple: false,
        allowedTypes: ['images'],
      },
      author: {
        type: 'relation',
        relation: 'manyToOne',
        target: 'plugin::users-permissions.user',
      },
      category: {
        type: 'relation',
        relation: 'manyToOne',
        target: 'api::category.category',
      },
      tags: {
        type: 'relation',
        relation: 'manyToMany',
        target: 'api::tag.tag',
      },
      seo: {
        type: 'component',
        component: 'shared.seo',
      },
      readTime: {
        type: 'integer',
        min: 1,
      },
      publishedAt: {
        type: 'datetime',
      },
      status: {
        type: 'enumeration',
        enum: ['draft', 'review', 'published', 'archived'],
        default: 'draft',
      },
    },
  },
  
  // Category Content Type
  'category': {
    kind: 'collectionType',
    collectionName: 'categories',
    info: {
      name: 'Category',
      description: 'Content categories',
    },
    attributes: {
      name: {
        type: 'string',
        required: true,
      },
      slug: {
        type: 'uid',
        targetField: 'name',
      },
      description: {
        type: 'text',
      },
      posts: {
        type: 'relation',
        relation: 'oneToMany',
        target: 'api::blog-post.blog-post',
        mappedBy: 'category',
      },
    },
  },
  
  // Page Content Type (Singleton)
  'page': {
    kind: 'collectionType',
    collectionName: 'pages',
    info: {
      name: 'Page',
      description: 'Static pages',
    },
    options: {
      draftAndPublish: true,
    },
    attributes: {
      title: {
        type: 'string',
        required: true,
      },
      slug: {
        type: 'uid',
        targetField: 'title',
      },
      content: {
        type: 'dynamiczone',
        components: [
          'sections.hero',
          'sections.feature-grid',
          'sections.text-image',
          'sections.cta',
        ],
      },
      seo: {
        type: 'component',
        component: 'shared.seo',
      },
    },
  },
};
"""
        
        files["components.js"] = """module.exports = {
  // SEO Component
  'shared.seo': {
    collectionName: 'components_shared_seos',
    info: {
      name: 'SEO',
      displayName: 'SEO',
      icon: 'search',
    },
    attributes: {
      metaTitle: {
        type: 'string',
        maxLength: 60,
      },
      metaDescription: {
        type: 'text',
        maxLength: 160,
      },
      keywords: {
        type: 'string',
      },
      metaImage: {
        type: 'media',
        multiple: false,
        allowedTypes: ['images'],
      },
      metaRobots: {
        type: 'string',
      },
      canonicalURL: {
        type: 'string',
      },
      structuredData: {
        type: 'json',
      },
    },
  },
  
  // Hero Section
  'sections.hero': {
    collectionName: 'components_sections_heroes',
    info: {
      name: 'Hero',
      displayName: 'Hero Section',
      icon: 'layout',
    },
    attributes: {
      heading: {
        type: 'string',
        required: true,
      },
      subheading: {
        type: 'text',
      },
      backgroundImage: {
        type: 'media',
        multiple: false,
        allowedTypes: ['images'],
      },
      ctaText: {
        type: 'string',
      },
      ctaLink: {
        type: 'string',
      },
      alignment: {
        type: 'enumeration',
        enum: ['left', 'center', 'right'],
        default: 'center',
      },
    },
  },
  
  // Feature Grid
  'sections.feature-grid': {
    collectionName: 'components_sections_feature_grids',
    info: {
      name: 'Feature Grid',
      displayName: 'Feature Grid',
      icon: 'grid',
    },
    attributes: {
      title: {
        type: 'string',
      },
      features: {
        type: 'component',
        component: 'elements.feature-item',
        repeat: true,
      },
      columns: {
        type: 'integer',
        min: 2,
        max: 4,
        default: 3,
      },
    },
  },
  
  // Feature Item
  'elements.feature-item': {
    collectionName: 'components_elements_feature_items',
    info: {
      name: 'Feature Item',
      displayName: 'Feature Item',
      icon: 'star',
    },
    attributes: {
      icon: {
        type: 'string',
      },
      title: {
        type: 'string',
        required: true,
      },
      description: {
        type: 'text',
      },
      link: {
        type: 'string',
      },
    },
  },
};
"""
        
        files["content-api.js"] = """// Content API Client

class ContentAPI {
  constructor(baseURL, apiToken = null) {
    this.baseURL = baseURL;
    this.apiToken = apiToken;
  }
  
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}/api${endpoint}`;
    
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };
    
    if (this.apiToken) {
      headers['Authorization'] = `Bearer ${this.apiToken}`;
    }
    
    const response = await fetch(url, {
      ...options,
      headers,
    });
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }
    
    return response.json();
  }
  
  // Get collection
  async getCollection(contentType, params = {}) {
    const query = new URLSearchParams();
    
    if (params.populate) query.set('populate', params.populate);
    if (params.filters) query.set('filters', JSON.stringify(params.filters));
    if (params.sort) query.set('sort', params.sort);
    if (params.pagination) {
      query.set('pagination[page]', params.pagination.page || 1);
      query.set('pagination[pageSize]', params.pagination.pageSize || 25);
    }
    if (params.fields) query.set('fields', params.fields.join(','));
    
    return this.request(`/${contentType}?${query.toString()}`);
  }
  
  // Get single entry
  async getEntry(contentType, id, params = {}) {
    const query = new URLSearchParams();
    if (params.populate) query.set('populate', params.populate);
    
    return this.request(`/${contentType}/${id}?${query.toString()}`);
  }
  
  // Get by slug
  async getBySlug(contentType, slug, params = {}) {
    const query = new URLSearchParams();
    query.set('filters[slug][$eq]', slug);
    if (params.populate) query.set('populate', params.populate);
    
    const result = await this.request(`/${contentType}?${query.toString()}`);
    return result.data?.[0] || null;
  }
  
  // Create entry
  async create(contentType, data) {
    return this.request(`/${contentType}`, {
      method: 'POST',
      body: JSON.stringify({ data }),
    });
  }
  
  // Update entry
  async update(contentType, id, data) {
    return this.request(`/${contentType}/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ data }),
    });
  }
  
  // Delete entry
  async delete(contentType, id) {
    return this.request(`/${contentType}/${id}`, {
      method: 'DELETE',
    });
  }
  
  // Search
  async search(contentType, query, fields = []) {
    const params = new URLSearchParams();
    
    fields.forEach((field, index) => {
      params.set(`filters[$or][${index}][${field}][$containsi]`, query);
    });
    
    return this.request(`/${contentType}?${params.toString()}`);
  }
}

// Usage example
// const cms = new ContentAPI('https://cms.example.com', 'your-api-token');
// const posts = await cms.getCollection('blog-posts', { 
//   populate: '*',
//   sort: 'publishedAt:desc',
//   pagination: { page: 1, pageSize: 10 }
// });

export default ContentAPI;
"""
        
        return files


def main():
    parser = argparse.ArgumentParser(description="🗂️ CMS-Agent — Content Management")
    parser.add_argument("request", nargs="?", help="Что создать")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = CMSAgent()
    
    if args.request:
        print(f"🗂️ {agent.NAME} создаёт: {args.request}")
        files = agent.process_request(args.request)
        
        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            for filename, content in files.items():
                filepath = output_dir / filename
                filepath.write_text(content, encoding="utf-8")
                print(f"✅ {filename}")
        else:
            for filename, content in files.items():
                print(f"\n{'='*50}")
                print(f"📄 {filename}")
                print('='*50)
                print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print(f"🗂️ {agent.NAME}")
        print(f"Роль: {agent.ROLE}")


if __name__ == "__main__":
    main()
