# 符号

本文档使用一些符号进行说明。在继续阅读之前，请确保您已经熟悉以下约定列表：

### <!-- md:sponsors --> – 仅限赞助商 { data-toc-label="Sponsors only" }

The pumping heart symbol denotes that a specific feature or behavior is only
available to sponsors via [Insiders]. Make sure that you have access to
[Insiders] if you want to use the feature.

### <!-- md:version --> – 版本 { #version data-toc-label="Version" }

The tag symbol in conjunction with a version number denotes when a specific
feature or behavior was added. Make sure you're at least on this version
if you want to use it.

### <!-- md:version insiders- --> – 版本 (内部)  { #version-insiders data-toc-label="Version (Insiders)" }

The tag symbol with a heart in conjunction with a version number denotes that a
specific feature or behavior was added to the [Insiders] version of Material for
MkDocs.

### <!-- md:default --> – 默认值 { #default data-toc-label="Default value" }

Some properties in `mkdocs.yml` have default values for when the author does not
explicitly define them. The default value of the property is always included.

#### <!-- md:default computed --> – 默认值是动态计算的 { #default data-toc-label="is computed" }

Some default values are not set to static values but computed from other values,
like the site language, repository provider, or other settings.

#### <!-- md:default none --> – 默认值为空 { #default data-toc-label="is empty" }

Some properties do not contain default values. This means that the functionality
that is associated with them is not available unless explicitly enabled.

### <!-- md:flag metadata --> – 元数据属性 { #metadata data-toc-label="Metadata property" }

This symbol denotes that the thing described is a metadata property, which can
be used in Markdown documents as part of the front matter definition.

### <!-- md:flag multiple --> – 多实例 { #multiple-instances data-toc-label="Multiple instances" }

This symbol denotes that the plugin supports multiple instances, i.e, that it
can be used multiple times in the `plugins` setting in `mkdocs.yml`.

### <!-- md:feature --> – 可选功能 { #feature data-toc-label="Optional feature" }

Most of the features are hidden behind feature flags, which means they must
be explicitly enabled via `mkdocs.yml`. This allows for the existence of
potentially orthogonal features.

### <!-- md:flag experimental --> – 实验性 { #experimental data-toc-label="Experimental" }

Some newer features are still considered experimental, which means they might
(although rarely) change at any time, including their complete removal (which
hasn't happened yet).

### <!-- md:plugin --> – 插件 { #plugin data-toc-label="Plugin" }

Several features are implemented through MkDocs excellent plugin architecture,
some of which are built-in and distributed with Material for MkDocs, so no
installation is required.

### <!-- md:extension --> – Markdown 扩展 { data-toc-label="Markdown extension" #extension }

This symbol denotes that the thing described is a Markdown extension, which can
be enabled in `mkdocs.yml` and adds additional functionality to the Markdown
parser.

### <!-- md:flag required --> – 必填的值 { #required data-toc-label="Required value" }

Some (very few in fact) properties or settings are required, which means the
authors must explicitly define them.

### <!-- md:flag customization --> – 定制 { #customization data-toc-label="Customization" }

This symbol denotes that the thing described is a customization that must be
added by the author.

### <!-- md:utility --> – 功能 { #utility data-toc-label="Utility" }

Besides plugins, there are some utilities that build on top of MkDocs in order
to provide extended functionality, like for example support for versioning.

  [Insiders]: about/sponsor.md

### <!-- md:locked --> - 不公开功能 { #locked }