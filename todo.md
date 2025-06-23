Things to do in webcowl
=======================

Desired features/improvements, in no particular order.

Owl
---

 * Read a directory of files instead of a single file
   * Add a selection menu to pick which file to display
 * Make boxes not change size when text gets wider
 * Display relative time since last data update
 * Indicate that web server is still sending data
   * Add a datastar signal for time of last update, and check that not too much time has elapsed?
   * Can a client automatically reconnect when server restarts?
 * Different ways to format values to string
   * Bitfield with characters for set/unset bits
   * value to string mapping (enum-like)
 * Different "limits", ways to change style based on value
   * Maybe integrate class into value to string format mapping. To not need parallel specs for values and limits
   * Add other types of limit conditions than gt, lt,  eq: like bitmask
   * way to add additional css files/classes outside of main webcowl.css
 * Read actual dirfiles
   * Maybe wait for pygetdata to be on pypi
 * Fancier grid layout
   * Want ability to reflow based on display width, but also to not waste much space with boxes of varying size

Cow
---

 * Disable  send button when there are errors for command parameters
 * Complex message builder
   * Instead of only send button, have a way to add commands into a larger messasge
 * Cow "awesome bar"
   * Search for commands, with live updates/autocomplete
   * Allow editing/pasting command in text format
 * Command logging
   * Eventually handle the fact that multiple cowl servers and command clients can exist. Need synchronization, or a central authority

General
-------

 * Login and authentication/authorization
   * sqlite database?
 * Integrate elog-like commands + human posts thing, with searching and filtering?
   * Like cow command logs, this will also need synchronization or a central authority
