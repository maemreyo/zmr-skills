# Blueprint and form contract

An assessment blueprint uses `schema_version: zamery-assessment-blueprint.v3`, a stable `blueprint_id`, and ordered sections. Every section has `section_id`, an exact positive `count`, and structured bank filters such as domain, skill, interaction, grade band, or difficulty range. Optional equivalence tolerances declare the permitted difference in mean difficulty across parallel forms.

A form manifest uses `schema_version: zamery-form.v3`, `form_id`, `blueprint_id`, integer `seed`, and ordered items. Each item snapshot preserves at least `item_id`, `version`, `section_id`, interaction, objective IDs, difficulty, and the approved content needed for projection.

Reproducibility requires the bank snapshot, blueprint, seed, and form IDs. A form is invalid if an item ID repeats, a stored version is missing, section counts drift, or the pool is too small. Never backfill from draft or retired items to make the count look complete.
