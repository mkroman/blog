+++
title = "Markdown frontmatter syntax highlighting for Vim and Neovim"
date = 2021-03-24

[taxonomies]
tags = ["neovim", "vim", "zola", "markdown"]
categories = ["programming"]
+++

The default markdown syntax highlighting configuration for Vim and Neovim does
not know how to highlight markdown frontmatter that is commonly used in static
site generators.

In this article I will show how you can add a syntax region that tells
Vim/Neovim to highlight the frontmatter with a different syntax.

<!-- more -->

The configuration is based on [this article][vim-markdown-frontmatter], which
you should also take a look at, as it will also tell you how you can fix
folding.

### The configuration

Both Vim and Neovim have the facility to extend syntax definitions by sourcing
config files in the users config folder.

This is done by creating a file in the `~/.vim/after/syntax/<syntax>.vim` for
Vim, and `~/.config/nvim/after/<syntax>.vim` for Neovim. In our case, `<syntax>`
is to replaced with `markdown`.

Since I'm using Neovim, and I'm using Zola as a static site generator (Zola uses
`+++` as starting and ending block for frontmatter, with a TOML syntax), I need
to write the following to my `~/.config/nvim/after/markdown.vim` file:

```vim
unlet b:current_syntax
syntax include @Toml syntax/toml.vim
syntax region tomlFrontmatter start=/\%^+++$/ end=/^+++$/ keepend contains=@Toml
```

However, if I were using a different static site generator where the frontmatter
block is defined with `---`, and the syntax was YAML, I would write:

```vim
unlet b:current_syntax
syntax include @Yaml syntax/yaml.vim
syntax region yamlFrontmatter start=/\%^---$/ end=/^---$/ keepend contains=@Yaml
```

### TL;DR

This is a combined configuration that *should* highlight `+++` frontmatter
blocks as TOML and `---` blocks as YAML.

Create the markdown syntax extension configuration (Neovim:
`~/.config/nvim/after/markdown.vim`, Vim: `~/.vim/after/markdown.vim`) with the
following contents:

```vim
unlet b:current_syntax
syntax include @Yaml syntax/yaml.vim
syntax include @Toml syntax/toml.vim
syntax region yamlFrontmatter start=/\%^---$/ end=/^---$/ keepend contains=@Yaml
syntax region tomlFrontmatter start=/\%^+++$/ end=/^+++$/ keepend contains=@Toml
```

[vim-markdown-frontmatter]: https://habamax.github.io/2019/03/07/vim-markdown-frontmatter.html

