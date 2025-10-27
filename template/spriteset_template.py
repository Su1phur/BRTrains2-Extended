PNML_TEMPLATE = """
// basic sprite
spriteset(spriteset_{unit}, "{path}/{unit}_1x_8bpp.png")
    {{ template_XXtrains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}, ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP, "{path}/{unit}_1x_32bpp.png", "{path}/{unit}_1x_mask.png")
    {{ template_XXtrains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}, ZOOM_LEVEL_IN_2X, BIT_DEPTH_32BPP, "{path}/{unit}_2x_32bpp.png", "{path}/{unit}_2x_mask.png")
    {{ template_XXtrains_2x(0,0) }}

    alternative_sprites(spriteset_{unit}, ZOOM_LEVEL_IN_4X, BIT_DEPTH_32BPP, "{path}/{unit}_4x_32bpp.png", "{path}/{unit}_4x_mask.png")
    {{ template_XXtrains_4x(0,0) }}

// purchase sprite
spriteset(spriteset_{unit}_purchase, "{path}/{unit}_1x_8bpp.png")
    {{ template_purchase(0,0) }}

    alternative_sprites(spriteset_{unit}_purchase, ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP, "{path}/{unit}_1x_32bpp.png", "{path}/{unit}_1x_mask.png")
    {{ template_purchase(0,0) }}
"""

LOADING_TEMPLATE = """
spriteset(spriteset_{unit}_Loading, "{path}/{unit}_Loading_1x_8bpp.png")
    {{ template_XXtrains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}_Loading, ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP, "{path}/{unit}_Loading_1x_32bpp.png", "{path}/{unit}_Loading_1x_mask.png")
    {{ template_XXtrains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}_Loading, ZOOM_LEVEL_IN_2X, BIT_DEPTH_32BPP, "{path}/{unit}_Loading_2x_32bpp.png", "{path}/{unit}_Loading_2x_mask.png")
    {{ template_XXtrains_2x(0,0) }}

    alternative_sprites(spriteset_{unit}_Loading, ZOOM_LEVEL_IN_4X, BIT_DEPTH_32BPP, "{path}/{unit}_Loading_4x_32bpp.png", "{path}/{unit}_Loading_4x_mask.png")
    {{ template_XXtrains_4x(0,0) }}

// loading sprite
spritegroup spritegroup_{unit}_Loading {{  
    loaded: [spriteset_empty];
    loading: [spriteset_{unit}_Loading]; }}

switch(FEAT_TRAINS, SELF, sw_loadstack_{unit}, [ STORE_TEMP((getbits(extra_callback_info1, 8, 8) < 1 ? CB_FLAG_MORE_SPRITES : 0) | PALETTE_USE_DEFAULT, 0x100), getbits(extra_callback_info1, 8, 8) ] ) {{
    0: spriteset_{unit};
    1: spritegroup_{unit}_Loading; }}
"""

CARGO_TEMPLATE = """
spriteset(spriteset_{unit}, "{path}/{unit}_1x_8bpp.png")
    {{ template_XXtrains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}, ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP, "{path}/{unit}_1x_32bpp.png", "{path}/{unit}_1x_mask.png")
    {{ template_XXtrains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}, ZOOM_LEVEL_IN_2X, BIT_DEPTH_32BPP, "{path}/{unit}_2x_32bpp.png", "{path}/{unit}_2x_mask.png")
    {{ template_XXtrains_2x(0,0) }}

    alternative_sprites(spriteset_{unit}, ZOOM_LEVEL_IN_4X, BIT_DEPTH_32BPP, "{path}/{unit}_4x_32bpp.png", "{path}/{unit}_4x_mask.png")
    {{ template_XXtrains_4x(0,0) }}

// loading sprite
spritegroup spritegroup_{unit} {{  
    loaded: [spriteset_empty, spriteset_{unit}];
    loading: [spriteset_empty, spriteset_{unit}]; }}

switch(FEAT_TRAINS, SELF, sw_loadstack_{unit}, [ STORE_TEMP((getbits(extra_callback_info1, 8, 8) < 1 ? CB_FLAG_MORE_SPRITES : 0) | PALETTE_USE_DEFAULT, 0x100), getbits(extra_callback_info1, 8, 8) ] ) {{
    0: spriteset_{base_unit};
    1: spritegroup_{unit}; }}
"""

BULK_TEMPLATE = """
spriteset(spriteset_{unit}, "{path}/{unit}_1x_8bpp.png")
    {{ template_XXtrains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}, ZOOM_LEVEL_IN_2X, BIT_DEPTH_8BPP, "{path}/{unit}_2x_8bpp.png")
    {{ template_XXtrains_2x(0,0) }}

    alternative_sprites(spriteset_{unit}, ZOOM_LEVEL_IN_4X, BIT_DEPTH_8BPP, "{path}/{unit}_4x_8bpp.png")
    {{ template_XXtrains_4x(0,0) }}
"""

BULK_SPRITEGROUP = """
// loading sprite
spritegroup spritegroup_{unit} {{  
    loaded: [spriteset_empty, spriteset_{unit}];
    loading: [spriteset_empty, spriteset_{unit}]; }}
"""

ANIM_TEMPLATE = """
// Anim_sprites
spriteset(spriteset_{unit}_Anim1, "{path}/{unit}_Anim_1_1x_8bpp.png")
    {{ template_XXtrains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}_Anim1, ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP, "{path}/{unit}_Anim_1_1x_32bpp.png", "{path}/{unit}_Anim_1_1x_mask.png")
    {{ template_XXtrains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}_Anim1, ZOOM_LEVEL_IN_2X, BIT_DEPTH_32BPP, "{path}/{unit}_Anim_1_2x_32bpp.png", "{path}/{unit}_Anim_1_2x_mask.png")
    {{ template_XXtrains_2x(0,0) }}

    alternative_sprites(spriteset_{unit}_Anim1, ZOOM_LEVEL_IN_4X, BIT_DEPTH_32BPP, "{path}/{unit}_Anim_1_4x_32bpp.png", "{path}/{unit}_Anim_1_4x_mask.png")
    {{ template_XXtrains_4x(0,0) }}

spriteset(spriteset_{unit}_Anim2, "{path}/{unit}_Anim_2_1x_8bpp.png")
    {{ template_XXtrains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}_Anim2, ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP, "{path}/{unit}_Anim_2_1x_32bpp.png", "{path}/{unit}_Anim_2_1x_mask.png")
    {{ template_XXtrains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}_Anim2, ZOOM_LEVEL_IN_2X, BIT_DEPTH_32BPP, "{path}/{unit}_Anim_2_2x_32bpp.png", "{path}/{unit}_Anim_2_2x_mask.png")
    {{ template_XXtrains_2x(0,0) }}

    alternative_sprites(spriteset_{unit}_Anim2, ZOOM_LEVEL_IN_4X, BIT_DEPTH_32BPP, "{path}/{unit}_Anim_2_4x_32bpp.png", "{path}/{unit}_Anim_2_4x_mask.png")
    {{ template_XXtrains_4x(0,0) }}

spriteset(spriteset_{unit}_Anim3, "{path}/{unit}_Anim_3_1x_8bpp.png")
    {{ template_XXtrains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}_Anim3, ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP, "{path}/{unit}_Anim_3_1x_32bpp.png", "{path}/{unit}_Anim_3_1x_mask.png")
    {{ template_XXtrains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}_Anim3, ZOOM_LEVEL_IN_2X, BIT_DEPTH_32BPP, "{path}/{unit}_Anim_3_2x_32bpp.png", "{path}/{unit}_Anim_3_2x_mask.png")
    {{ template_XXtrains_2x(0,0) }}

    alternative_sprites(spriteset_{unit}_Anim3, ZOOM_LEVEL_IN_4X, BIT_DEPTH_32BPP, "{path}/{unit}_Anim_3_4x_32bpp.png", "{path}/{unit}_Anim_3_4x_mask.png")
    {{ template_XXtrains_4x(0,0) }}

spriteset(spriteset_{unit}_Anim4, "{path}/{unit}_Anim_4_1x_8bpp.png")
    {{ template_XXtrains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}_Anim4, ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP, "{path}/{unit}_Anim_4_1x_32bpp.png", "{path}/{unit}_Anim_4_1x_mask.png")
    {{ template_XXtrains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}_Anim4, ZOOM_LEVEL_IN_2X, BIT_DEPTH_32BPP, "{path}/{unit}_Anim_4_2x_32bpp.png", "{path}/{unit}_Anim_4_2x_mask.png")
    {{ template_XXtrains_2x(0,0) }}

    alternative_sprites(spriteset_{unit}_Anim4, ZOOM_LEVEL_IN_4X, BIT_DEPTH_32BPP, "{path}/{unit}_Anim_4_4x_32bpp.png", "{path}/{unit}_Anim_4_4x_mask.png")
    {{ template_XXtrains_4x(0,0) }}

spriteset(spriteset_{unit}_Anim_purchase, "{path}/{unit}_Anim_1_1x_8bpp.png")
    {{ template_purchase(0,0) }}

    alternative_sprites(spriteset_{unit}_Anim_purchase, ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP, "{path}/{unit}_Anim_1_1x_32bpp.png", "{path}/{unit}_Anim_1_1x_mask.png")
    {{ template_purchase(0,0) }}

switch(FEAT_TRAINS, SELF, sw_animation_{unit}, motion_counter % 4) {{
    0: spriteset_{unit}_Anim1;
    1: spriteset_{unit}_Anim2;
    2: spriteset_{unit}_Anim3;
    3: spriteset_{unit}_Anim4; }}

switch(FEAT_TRAINS, SELF, sw_animation_{unit}_REV, motion_counter % 4) {{
    0: spriteset_{unit}_Anim1;
    1: spriteset_{unit}_Anim4;
    2: spriteset_{unit}_Anim3;
    3: spriteset_{unit}_Anim2; }}

switch(FEAT_TRAINS, SELF, sw_pick_animation_{unit}, vehicle_is_reversed) {{
    0:  sw_animation_{unit};
        sw_animation_{unit}_REV; }}

switch(FEAT_TRAINS, SELF, sw_spritestack_{unit}_purchase, [ STORE_TEMP((getbits(extra_callback_info1, 8, 8) < 1 ? CB_FLAG_MORE_SPRITES : 0) | PALETTE_USE_DEFAULT, 0x100), getbits(extra_callback_info1, 8, 8) ] ) {{
    0: spriteset_{unit};
    1: spriteset_{unit}_Anim_purchase; }}
"""

DUAL_MODE_TEMPLATE = """
// pantograph sprite
spriteset(spriteset_{unit}_panto_up, "{path}/{unit}_panto_up_1x_8bpp.png")
    {{ template_XXtrains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}_panto_up, ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP, "{path}/{unit}_panto_up_1x_32bpp.png", "{path}/{unit}_panto_up_1x_mask.png")
    {{ template_XXtrains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}_panto_up, ZOOM_LEVEL_IN_2X, BIT_DEPTH_32BPP, "{path}/{unit}_panto_up_2x_32bpp.png", "{path}/{unit}_panto_up_2x_mask.png")
    {{ template_XXtrains_2x(0,0) }}

    alternative_sprites(spriteset_{unit}_panto_up, ZOOM_LEVEL_IN_4X, BIT_DEPTH_32BPP, "{path}/{unit}_panto_up_4x_32bpp.png", "{path}/{unit}_panto_up_4x_mask.png")
    {{ template_XXtrains_4x(0,0) }}

spriteset(spriteset_{unit}_panto_down, "{path}/{unit}_panto_down_1x_8bpp.png")
    {{ template_XXtrains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}_panto_down, ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP, "{path}/{unit}_panto_down_1x_32bpp.png", "{path}/{unit}_panto_down_1x_mask.png")
    {{ template_XXtrains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}_panto_down, ZOOM_LEVEL_IN_2X, BIT_DEPTH_32BPP, "{path}/{unit}_panto_down_2x_32bpp.png", "{path}/{unit}_panto_down_2x_mask.png")
    {{ template_XXtrains_2x(0,0) }}

    alternative_sprites(spriteset_{unit}_panto_down, ZOOM_LEVEL_IN_4X, BIT_DEPTH_32BPP, "{path}/{unit}_panto_down_4x_32bpp.png", "{path}/{unit}_panto_down_4x_mask.png")
    {{ template_XXtrains_4x(0,0) }}

spriteset(spriteset_{unit}_panto_down_purchase, "{path}/{unit}_panto_down_1x_8bpp.png")
    {{ template_purchase(0,0) }}

    alternative_sprites(spriteset_{unit}_panto_down_purchase, ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP, "{path}/{unit}_panto_down_1x_32bpp.png", "{path}/{unit}_panto_down_1x_mask.png")
    {{ template_purchase(0,0) }}

    
// dual mode switches
switch(FEAT_TRAINS, SELF, sw_spritestack_{unit}_purchase, [STORE_TEMP((getbits(extra_callback_info1, 8, 8) < 1 ? CB_FLAG_MORE_SPRITES : 0) | PALETTE_USE_DEFAULT, 0x100), getbits(extra_callback_info1, 8, 8)]) {{
    0: spriteset_{unit}_purchase;
    1: spriteset_{unit}_panto_down_purchase; }}
							
switch(FEAT_TRAINS, PARENT, sw_panto_{unit}, tile_powers_railtype("ELRL")) {{
    1: return spriteset_{unit}_panto_up;
        return spriteset_{unit}_panto_down; }}	
        
switch(FEAT_TRAINS, PARENT, sw_power_{unit}, tile_powers_railtype("ELRL")){{
    1: ;
        ; }}

switch(FEAT_TRAINS, SELF, sw_spritestack_{unit}, [STORE_TEMP((getbits(extra_callback_info1, 8, 8) < 1 ? CB_FLAG_MORE_SPRITES : 0) | PALETTE_USE_DEFAULT, 0x100), getbits(extra_callback_info1, 8, 8)]) {{
    0: spriteset_{unit};
    1: return sw_panto_{unit}; }}
"""