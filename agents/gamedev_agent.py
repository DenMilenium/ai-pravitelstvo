#!/usr/bin/env python3
"""
🎮 GameDev-Agent
Game Developer агент

Создаёт:
- Игры на Unity
- Godot проекты
- Game logic
- Game assets
"""

import argparse
from pathlib import Path
from typing import Dict


class GameDevAgent:
    """
    🎮 GameDev-Agent
    
    Специализация: Game Development
    Стек: Unity, Godot, Game Logic
    """
    
    NAME = "🎮 GameDev-Agent"
    ROLE = "Game Developer"
    EXPERTISE = ["Unity", "Godot", "C#", "GDScript", "Game Logic"]
    
    def process_request(self, request: str, engine: str = "godot") -> Dict[str, str]:
        files = {}
        
        if engine == "unity":
            files = self._generate_unity(request)
        else:
            files = self._generate_godot(request)
        
        return files
    
    def _generate_godot(self, game: str) -> Dict[str, str]:
        files = {}
        
        files["project.godot"] = """; Engine Configuration File
; Godot version: 4.x

[application]
config/name="MyGame"
config/description="Game created by GameDev-Agent"
run/main_scene="res://scenes/main.tscn"
config/features=PackedStringArray("4.2", "Mobile")
config/icon="res://icon.svg"

[display]
window/size/viewport_width=1280
window/size/viewport_height=720
window/stretch/mode="canvas_items"

[input]
move_left={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":65,"key_label":0,"unicode":97,"echo":false,"script":null)
]
}
move_right={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":68,"key_label":0,"unicode":100,"echo":false,"script":null)
]
}
jump={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":32,"key_label":0,"unicode":32,"echo":false,"script":null)
]
}

[rendering]
renderer/rendering_method="mobile"
textures/vram_compression/import_etc2_astc=true
"""
        
        files["player.gd"] = """extends CharacterBody2D

@export var speed: float = 300.0
@export var jump_velocity: float = -400.0
@export var gravity: float = 980.0

@onready var sprite = $Sprite2D
@onready var animation_player = $AnimationPlayer

func _physics_process(delta):
    # Apply gravity
    if not is_on_floor():
        velocity.y += gravity * delta
    
    # Handle jump
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity
        play_animation("jump")
    
    # Handle horizontal movement
    var direction = Input.get_axis("move_left", "move_right")
    
    if direction:
        velocity.x = direction * speed
        sprite.flip_h = direction < 0
        if is_on_floor():
            play_animation("run")
    else:
        velocity.x = move_toward(velocity.x, 0, speed)
        if is_on_floor():
            play_animation("idle")
    
    move_and_slide()

func play_animation(anim_name: String):
    if animation_player.has_animation(anim_name):
        animation_player.play(anim_name)
"""
        
        files["main.tscn"] = """[gd_scene load_steps=4 format=3 uid="uid://main"]

[ext_resource type="Script" path="res://player.gd" id="1_player"]

[sub_resource type="RectangleShape2D" id="player_shape"]
size = Vector2(32, 32)

[sub_resource type="PlaceholderTexture2D" id="player_tex"]
size = Vector2(32, 32)

[node name="Main" type="Node2D"]

[node name="Player" type="CharacterBody2D" parent="."]
position = Vector2(100, 300)
script = ExtResource("1_player")

[node name="Sprite2D" type="Sprite2D" parent="Player"]
texture = SubResource("player_tex")

[node name="CollisionShape2D" type="CollisionShape2D" parent="Player"]
shape = SubResource("player_shape")

[node name="Camera2D" type="Camera2D" parent="Player"]
position_smoothing_enabled = true

[node name="Ground" type="StaticBody2D" parent="."]
position = Vector2(400, 500)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Ground"]
shape = SubResource("player_shape")

[node name="Sprite2D" type="Sprite2D" parent="Ground"]
modulate = Color(0.2, 0.5, 0.2, 1)
texture = SubResource("player_tex")
"""
        
        return files
    
    def _generate_unity(self, game: str) -> Dict[str, str]:
        files = {}
        
        files["PlayerController.cs"] = """using UnityEngine;

public class PlayerController : MonoBehaviour
{
    [SerializeField] private float moveSpeed = 5f;
    [SerializeField] private float jumpForce = 10f;
    [SerializeField] private LayerMask groundLayer;
    
    private Rigidbody2D rb;
    private SpriteRenderer spriteRenderer;
    private bool isGrounded;
    private float horizontalInput;
    
    private void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        spriteRenderer = GetComponent<SpriteRenderer>();
    }
    
    private void Update()
    {
        // Get input
        horizontalInput = Input.GetAxisRaw("Horizontal");
        
        // Check grounded
        isGrounded = Physics2D.OverlapCircle(transform.position, 0.2f, groundLayer);
        
        // Jump
        if (Input.GetButtonDown("Jump") && isGrounded)
        {
            rb.velocity = new Vector2(rb.velocity.x, jumpForce);
        }
        
        // Flip sprite
        if (horizontalInput > 0)
            spriteRenderer.flipX = false;
        else if (horizontalInput < 0)
            spriteRenderer.flipX = true;
    }
    
    private void FixedUpdate()
    {
        // Move
        rb.velocity = new Vector2(horizontalInput * moveSpeed, rb.velocity.y);
    }
}
"""
        
        return files


def main():
    parser = argparse.ArgumentParser(description="🎮 GameDev-Agent — Games")
    parser.add_argument("request", nargs="?", help="Что создать")
    parser.add_argument("--engine", "-e", default="godot", choices=["godot", "unity"])
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = GameDevAgent()
    
    if args.request:
        print(f"🎮 {agent.NAME} создаёт: {args.request}")
        files = agent.process_request(args.request, args.engine)
        
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
        print(f"🎮 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")


if __name__ == "__main__":
    main()
