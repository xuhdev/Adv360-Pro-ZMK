#!/bin/env python3

"""
Use this script by running

    python3 gen_keymap.py > adv360.keymap
"""

import csv
import io

KEYMAP_FILE_TEMPLATE = '''
#include <behaviors.dtsi>
#include <dt-bindings/zmk/keys.h>
#include <dt-bindings/zmk/bt.h>
#include <dt-bindings/zmk/rgb.h>
#include <dt-bindings/zmk/stp.h>
#include <dt-bindings/zmk/backlight.h>
#define ZMK_POINTING_DEFAULT_MOVE_VAL 1500  // default: 600
#define ZMK_POINTING_DEFAULT_SCRL_VAL 60    // default: 10
#include <dt-bindings/zmk/pointing.h>

{layer_macros}

#define RMODS MOD_RCTL|MOD_RGUI|MOD_RALT|MOD_RSFT
#define LMODS MOD_LCTL|MOD_LGUI|MOD_LALT|MOD_LSFT

&caps_word {{
    continue-list = <UNDERSCORE MINUS BACKSPACE DELETE>;
}};

/ {{
    behaviors {{
      #include "macros.dtsi"
      #include "version.dtsi"

      hm: homerow_mods {{
          compatible = "zmk,behavior-hold-tap";
          label = "HOMEROW_MODS";
          #binding-cells = <2>;
          tapping-term-ms = <300>;
          quick_tap_ms = <275>;
          require-prior-idle-ms = <0>;
          flavor = "balanced";
          bindings = <&kp>, <&kp>;
      }};

      // Individual homerow mods. They forbid a left modifier to be combined
      // with a right modifier to increase accuracy in typing modifier + a
      // homerow key, such as Shift+A, Ctrl+F, Ctrl+L, etc.
      hmlshift: hm_left_shift {{
          compatible = "zmk,behavior-mod-morph";
          #binding-cells = <0>;
          bindings = <&hm LSHIFT A>, <&kp A>;
          mods = <(RMODS)>;
          keep-mods = <(RMODS)>;
      }};

      hmrshift: hm_right_shift {{
          compatible = "zmk,behavior-mod-morph";
          #binding-cells = <0>;
          bindings = <&hm RSHIFT SEMI>, <&kp SEMI>;
          mods = <(LMODS)>;
          keep-mods = <(LMODS)>;
      }};

      hmlshifttab: hm_left_shift_tab {{
          compatible = "zmk,behavior-mod-morph";
          #binding-cells = <0>;
          bindings = <&hm LSHIFT TAB>, <&kp TAB>;
          mods = <(RMODS)>;
          keep-mods = <(RMODS)>;
      }};

      hmrshiftbackslash: hm_right_shift_backslash {{
          compatible = "zmk,behavior-mod-morph";
          #binding-cells = <0>;
          bindings = <&hm RSHIFT BSLH>, <&kp BSLH>;
          mods = <(LMODS)>;
          keep-mods = <(LMODS)>;
      }};

      hmlctrl: hm_left_ctrl {{
          compatible = "zmk,behavior-mod-morph";
          #binding-cells = <0>;
          bindings = <&hm LCTRL F>, <&kp F>;
          mods = <(RMODS)>;
          keep-mods = <(RMODS)>;
      }};

      hmrctrl: hm_right_ctrl {{
          compatible = "zmk,behavior-mod-morph";
          #binding-cells = <0>;
          bindings = <&hm RCTRL J>, <&kp J>;
          mods = <(LMODS)>;
          keep-mods = <(LMODS)>;
      }};

      hmlgui: hm_left_gui {{
          compatible = "zmk,behavior-mod-morph";
          #binding-cells = <0>;
          bindings = <&hm LGUI D>, <&kp D>;
          mods = <(RMODS)>;
          keep-mods = <(RMODS)>;
      }};

      hmrgui: hm_right_gui {{
          compatible = "zmk,behavior-mod-morph";
          #binding-cells = <0>;
          bindings = <&hm RGUI K>, <&kp K>;
          mods = <(LMODS)>;
          keep-mods = <(LMODS)>;
      }};

      hmlalt: hm_left_alt {{
          compatible = "zmk,behavior-mod-morph";
          #binding-cells = <0>;
          bindings = <&hm LALT S>, <&kp S>;
          mods = <(RMODS)>;
          keep-mods = <(RMODS)>;
      }};

      hmralt: hm_right_alt {{
          compatible = "zmk,behavior-mod-morph";
          #binding-cells = <0>;
          bindings = <&hm RALT L>, <&kp L>;
          mods = <(LMODS)>;
          keep-mods = <(LMODS)>;
      }};

      tm: thumb_mods {{
          compatible = "zmk,behavior-hold-tap";
          label = "THUMB_MODS";
          #binding-cells = <2>;
          tapping-term-ms = <200>;
          quick_tap_ms = <175>;
          require-prior-idle-ms = <125>;
          flavor = "balanced";
          bindings = <&mo>, <&kp>;
      }};

      mlm: mouse_layer_mods {{
          compatible = "zmk,behavior-hold-tap";
          label = "MOUSE_LAYER_MODS";
          #binding-cells = <2>;
          tapping-term-ms = <200>;
          flavor = "hold-preferred";
          bindings = <&mo>, <&tog>;
      }};
    }};

    macros {{
        mcr_thanks: mcr_thanks {{
            compatible = "zmk,behavior-macro";
            #binding-cells = <0>;
            bindings
                = <&macro_press &kp RSHFT>
                , <&macro_tap &kp T>
                , <&macro_release &kp RSHFT>
                , <&macro_tap &kp H &kp A &kp N &kp K &kp S>
                ;
        }};
        mcr_sg: mcr_sounds_good {{
            compatible = "zmk,behavior-macro";
            #binding-cells = <0>;
            bindings
                = <&macro_press &kp RSHFT>
                , <&macro_tap &kp S>
                , <&macro_release &kp RSHFT>
                , <&macro_tap &kp O &kp U &kp N &kp D &kp S &kp SPACE &kp G &kp O &kp O &kp D &kp EXCLAMATION>
                ;
        }};
        mcr_np: mcr_no_problem {{
            compatible = "zmk,behavior-macro";
            #binding-cells = <0>;
            bindings
                = <&macro_press &kp RSHFT>
                , <&macro_tap &kp N>
                , <&macro_release &kp RSHFT>
                , <&macro_tap &kp O &kp SPACE &kp P &kp R &kp O &kp B &kp L &kp E &kp M &kp EXCLAMATION>
                ;
        }};
    }};

    keymap {{
        compatible = "zmk,keymap";
        {keymaps}
    }};
}};
'''


LAYERS = ("Base",
          "Extra White", "Extra Blue", "Extra Green", "Extra Red",
          "Secondary Left", "Secondary Right",
          "Media", "Mouse", "Mod", "Original")


def gen_layer(name: str, display_name: str, bindings: str):
    """Generate a layer."""
    return f'''
    {name} {{
      display-name = "{display_name}";
      bindings = <
        {bindings}
      >;
    }};
    '''


def gen_keymaps():
    """Generate keymaps."""
    keymaps = io.StringIO()

    for i, layer in enumerate(LAYERS):
        layer_name = layer.lower().replace(' ', '_')
        layer_display_name = layer

        bindings = io.StringIO()
        with open(f'{layer_name}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                print('\t'.join(row), file=bindings)

        keymaps.write(
            gen_layer(layer_name, layer_display_name, bindings.getvalue()))

    return keymaps.getvalue()


def gen_keymap_file():
    """Generate the keymap file."""
    layer_macros = '\n'.join(
        f"#define LAYER_{layer.upper().replace(' ', '_')} {i}"
        for i, layer in enumerate(LAYERS))
    return KEYMAP_FILE_TEMPLATE.format(
        layer_macros=layer_macros, keymaps=gen_keymaps())


if __name__ == '__main__':
    print(gen_keymap_file())
