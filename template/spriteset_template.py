PNML_TEMPLATE = """
// basic sprite
spriteset(spriteset_{unit}, "{path}\\{unit}_1x_8bpp.png")
    {{ template_trains_1x(0,0) }}

alternative_sprites(spriteset_{unit}, ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP, "{path}\\{unit}_1x_32bpp.png", "{path}\\{unit}_1x_mask.png")
    {{ template_trains_1x(0,0) }}

alternative_sprites(spriteset_{unit}, ZOOM_LEVEL_IN_2X, BIT_DEPTH_32BPP, "{path}\\{unit}_2x_32bpp.png", "{path}\\{unit}_2x_mask.png")
    {{ template_trains_2x(0,0) }}

alternative_sprites(spriteset_{unit}, ZOOM_LEVEL_IN_4X, BIT_DEPTH_32BPP, "{path}\\{unit}_4x_32bpp.png", "{path}\\{unit}_4x_mask.png")
    {{ template_trains_4x(0,0) }}
"""

LOADING_TEMPLATE = """
spriteset(spriteset_{unit}_Loading, "{path}\\{unit}_Loading_1x_8bpp.png")
    {{ template_trains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}_Loading, ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP, "{path}\\{unit}_Loading_1x_32bpp.png", "{path}\\{unit}_Loading_1x_mask.png")
    {{ template_trains_1x(0,0) }}

    alternative_sprites(spriteset_{unit}_Loading, ZOOM_LEVEL_IN_2X, BIT_DEPTH_32BPP, "{path}\\{unit}_Loading_2x_32bpp.png", "{path}\\{unit}_Loading_2x_mask.png")
    {{ template_trains_2x(0,0) }}

    alternative_sprites(spriteset_{unit}_Loading, ZOOM_LEVEL_IN_4X, BIT_DEPTH_32BPP, "{path}\\{unit}_Loading_4x_32bpp.png", "{path}\\{unit}_Loading_4x_mask.png")
    {{ template_trains_4x(0,0) }}


// loading sprite
spritegroup spritegroup_{unit}_Loading {  
    loaded: [spriteset_empty];
    loading: [spriteset_{unit}_Loading]; }

switch(FEAT_TRAINS, SELF, sw_loadstack_{unit}, [ STORE_TEMP((getbits(extra_callback_info1, 8, 8) < 1 ? CB_FLAG_MORE_SPRITES : 0) | PALETTE_USE_DEFAULT, 0x100), getbits(extra_callback_info1, 8, 8) ] ) {
    0: spriteset_{unit};
    1: spritegroup_{unit}_Loading; }
"""