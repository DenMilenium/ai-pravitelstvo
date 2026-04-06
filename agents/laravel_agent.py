#!/usr/bin/env python3
"""
🚀 Laravel-Agent
Laravel Developer агент

Создаёт:
- Laravel проекты
- Laravel API
- Eloquent модели
- Blade шаблоны
"""

import argparse
from pathlib import Path
from typing import Dict


class LaravelAgent:
    """
    🚀 Laravel-Agent
    
    Специализация: Laravel Development
    Стек: Laravel, PHP, Eloquent, Blade
    """
    
    NAME = "🚀 Laravel-Agent"
    ROLE = "Laravel Developer"
    EXPERTISE = ["Laravel", "PHP", "Eloquent", "Blade", "Livewire"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["User.php"] = """<?php

namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Factories\\HasFactory;
use Illuminate\\Foundation\\Auth\\User as Authenticatable;
use Illuminate\\Notifications\\Notifiable;
use Illuminate\\Database\\Eloquent\\Relations\\HasMany;
use Illuminate\\Database\\Eloquent\\Relations\\BelongsToMany;
use Laravel\\Sanctum\\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;

    protected $fillable = [
        'name',
        'email',
        'password',
        'avatar',
        'bio',
        'is_verified',
    ];

    protected $hidden = [
        'password',
        'remember_token',
    ];

    protected $casts = [
        'email_verified_at' => 'datetime',
        'password' => 'hashed',
        'is_verified' => 'boolean',
    ];

    protected $appends = ['avatar_url'];

    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }

    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }

    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class);
    }

    public function getAvatarUrlAttribute(): ?string
    {
        return $this->avatar ? asset('storage/' . $this->avatar) : null;
    }

    public function hasRole(string $role): bool
    {
        return $this->roles->contains('slug', $role);
    }

    public function scopeVerified($query)
    {
        return $query->where('is_verified', true);
    }
}
"""
        
        files["Post.php"] = """<?php

namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Factories\\HasFactory;
use Illuminate\\Database\\Eloquent\\Model;
use Illuminate\\Database\\Eloquent\\Relations\\BelongsTo;
use Illuminate\\Database\\Eloquent\\Relations\\HasMany;
use Illuminate\\Database\\Eloquent\\Relations\\BelongsToMany;
use Illuminate\\Support\\Str;

class Post extends Model
{
    use HasFactory;

    protected $fillable = [
        'title',
        'slug',
        'content',
        'excerpt',
        'featured_image',
        'user_id',
        'category_id',
        'status',
        'published_at',
    ];

    protected $casts = [
        'published_at' => 'datetime',
        'is_published' => 'boolean',
    ];

    protected static function boot()
    {
        parent::boot();

        static::creating(function ($post) {
            if (empty($post->slug)) {
                $post->slug = Str::slug($post->title);
            }
        });
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function category(): BelongsTo
    {
        return $this->belongsTo(Category::class);
    }

    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }

    public function tags(): BelongsToMany
    {
        return $this->belongsToMany(Tag::class);
    }

    public function scopePublished($query)
    {
        return $query->where('status', 'published')
            ->whereNotNull('published_at')
            ->where('published_at', '<=', now());
    }

    public function scopeDraft($query)
    {
        return $query->where('status', 'draft');
    }

    public function getRouteKeyName(): string
    {
        return 'slug';
    }

    public function getReadingTimeAttribute(): int
    {
        $words = str_word_count(strip_tags($this->content));
        return ceil($words / 200);
    }
}
"""
        
        files["PostController.php"] = """<?php

namespace App\\Http\\Controllers\\Api;

use App\\Http\\Controllers\\Controller;
use App\\Models\\Post;
use App\\Http\\Resources\\PostResource;
use App\\Http\\Requests\\StorePostRequest;
use App\\Http\\Requests\\UpdatePostRequest;
use Illuminate\\Http\\Request;
use Illuminate\\Http\\Resources\\Json\\AnonymousResourceCollection;
use Illuminate\\Support\\Facades\\Auth;

class PostController extends Controller
{
    public function index(Request $request): AnonymousResourceCollection
    {
        $posts = Post::with(['user', 'category', 'tags'])
            ->published()
            ->when($request->category, function ($query, $category) {
                return $query->whereHas('category', function ($q) use ($category) {
                    $q->where('slug', $category);
                });
            })
            ->when($request->search, function ($query, $search) {
                return $query->where(function ($q) use ($search) {
                    $q->where('title', 'like', "%{$search}%")
                        ->orWhere('content', 'like', "%{$search}%");
                });
            })
            ->latest('published_at')
            ->paginate($request->get('per_page', 10));

        return PostResource::collection($posts);
    }

    public function store(StorePostRequest $request): PostResource
    {
        $post = Auth::user()->posts()->create($request->validated());

        if ($request->has('tags')) {
            $post->tags()->sync($request->tags);
        }

        return new PostResource($post->load('user', 'category', 'tags'));
    }

    public function show(Post $post): PostResource
    {
        $post->increment('views');
        return new PostResource($post->load('user', 'category', 'tags', 'comments'));
    }

    public function update(UpdatePostRequest $request, Post $post): PostResource
    {
        $this->authorize('update', $post);

        $post->update($request->validated());

        if ($request->has('tags')) {
            $post->tags()->sync($request->tags);
        }

        return new PostResource($post->load('user', 'category', 'tags'));
    }

    public function destroy(Post $post)
    {
        $this->authorize('delete', $post);

        $post->delete();

        return response()->json(['message' => 'Post deleted successfully']);
    }

    public function myPosts(Request $request): AnonymousResourceCollection
    {
        $posts = Auth::user()->posts()
            ->with(['category', 'tags'])
            ->latest()
            ->paginate($request->get('per_page', 10));

        return PostResource::collection($posts);
    }

    public function publish(Post $post): PostResource
    {
        $this->authorize('update', $post);

        $post->update([
            'status' => 'published',
            'published_at' => now(),
        ]);

        return new PostResource($post);
    }
}
"""
        
        files["api-routes.php"] = """<?php

use Illuminate\\Support\\Facades\\Route;
use App\\Http\\Controllers\\Api\\PostController;
use App\\Http\\Controllers\\Api\\CategoryController;
use App\\Http\\Controllers\\Api\\CommentController;
use App\\Http\\Controllers\\Api\\AuthController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
*/

// Public routes
Route::get('/posts', [PostController::class, 'index']);
Route::get('/posts/{post}', [PostController::class, 'show']);
Route::get('/categories', [CategoryController::class, 'index']);
Route::get('/categories/{category}', [CategoryController::class, 'show']);

// Authentication
Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login']);
Route::post('/forgot-password', [AuthController::class, 'forgotPassword']);
Route::post('/reset-password', [AuthController::class, 'resetPassword']);

// Protected routes
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/user', [AuthController::class, 'user']);
    Route::post('/logout', [AuthController::class, 'logout']);
    
    // Posts
    Route::post('/posts', [PostController::class, 'store']);
    Route::put('/posts/{post}', [PostController::class, 'update']);
    Route::delete('/posts/{post}', [PostController::class, 'destroy']);
    Route::post('/posts/{post}/publish', [PostController::class, 'publish']);
    Route::get('/my-posts', [PostController::class, 'myPosts']);
    
    // Comments
    Route::post('/posts/{post}/comments', [CommentController::class, 'store']);
    Route::delete('/comments/{comment}', [CommentController::class, 'destroy']);
});
"""
        
        return files


def main():
    parser = argparse.ArgumentParser(description="🚀 Laravel-Agent — Laravel/PHP")
    parser.add_argument("request", nargs="?", help="Что создать")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = LaravelAgent()
    
    if args.request:
        print(f"🚀 {agent.NAME} создаёт: {args.request}")
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
        print(f"🚀 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")


if __name__ == "__main__":
    main()
