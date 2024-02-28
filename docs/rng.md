---
title: RNG Commands
icon: material/dice-multiple-outline
---

## Slash Commands

### [:material-slash-forward-box:][slash]`pick <choices>`

:   Randomly chooses an option from a comma-separated list.

    ``` cirru
    /pick choices: coffee, tea, snail
    ```

    ```
    snail
    ```

---

### [:material-slash-forward-box:][slash]`pickmember`

:   Randomly chooses a member of the server.

    ``` cirru
    /pickmember
    ```

    ```
    elliejb
    ```

---

### [:material-slash-forward-box:][slash]`rng <min> <max>`

:   Randomly picks a number from `min` to `max`, including `min` and `max`.

    ``` cirru
    /rng min: 10 max: 15
    ```

    ```
    11
    ```

---

[slash]: https://support.discord.com/hc/en-us/articles/1500000368501-Slash-Commands-FAQ "Slash Command"