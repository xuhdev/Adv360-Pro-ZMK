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
#include <dt-bindings/zmk/pointing.h>

{layer_macros}

/ {{
    behaviors {{
      #include "macros.dtsi"
      #include "version.dtsi"

      hm: homerow_mods {{
          compatible = "zmk,behavior-hold-tap";
          label = "HOMEROW_MODS";
          #binding-cells = <2>;
          tapping-term-ms = <250>;
          quick_tap_ms = <225>;
          flavor = "tap-preferred";
          bindings = <&kp>, <&kp>;
      }};

      tm: thumb_mods {{
          compatible = "zmk,behavior-hold-tap";
          label = "THUMB_MODS";
          #binding-cells = <2>;
          tapping-term-ms = <250>;
          quick_tap_ms = <225>;
          flavor = "tap-preferred";
          bindings = <&mo>, <&kp>;
      }};
    }};

  keymap {{
    compatible = "zmk,keymap";
    {keymaps}
  }};
}};
'''


LAYERS = ("Base", "Secondary Left", "Secondary Right",
          "Media", "Mod", "Original")


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
