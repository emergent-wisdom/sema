# Vocabulary data

`taxonomy.db` is the authoritative Sema bootstrap vocabulary. It is the only
database bundled with the package and the only database used by the built-in
`full` and `standard` presets.

`experimental.db` is a deprecated, frozen snapshot from the former experimental
shelf. It is retained in the repository for historical review only. It is not
maintained, packaged, or selected by any built-in Sema tooling. Any future
experimental vocabulary will be reviewed and published as a new versioned
library rather than reviving this snapshot.
