from scripts.game.characters.marisa import speed as marisa_speed, spritesheet as marisa_spritesheet, bulletSpritesheet as marisa_bulletSpritesheet, attack as marisa_attack

characters = {
    0: {
        "name": "Marisa",
        "speed": marisa_speed,
        "sprite-sheet": marisa_spritesheet,
        "bullet-sprite-sheet": marisa_bulletSpritesheet,
        "attack-function": marisa_attack
    },
}