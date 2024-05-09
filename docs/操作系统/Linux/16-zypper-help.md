# zypper help

<span style="color:rgb(100,180,246);font-size:11pt">最后更新：2017-06-27</span>

```
zypper help 
  Usage: 
        zypper [--global-options] <command> [--command-options] [arguments] 

  Global Options: 
        --help, -h              Help. 
        --version, -V           Output the version number. 
        --promptids             Output a list of zypper's user prompts. 
        --config, -c <file>     Use specified config file instead of the default. 
        --userdata <string>     User defined transaction id used in history and plugins. 
        --quiet, -q             Suppress normal output, print only error 
                                messages. 
        --verbose, -v           Increase verbosity. 
        --no-abbrev, -A         Do not abbreviate text in tables. 
        --table-style, -s       Table style (integer). 
        --rug-compatible, -r    Turn on rug compatibility. 
        --non-interactive, -n   Do not ask anything, use default answers 
                                automatically. 
        --non-interactive-include-reboot-patches 
                                Do not treat patches as interactive, which have 
                                the rebootSuggested-flag set. 
        --xmlout, -x            Switch to XML output. 

        --reposd-dir, -D <dir>  Use alternative repository definition file 
                                directory. 
        --cache-dir, -C <dir>   Use alternative directory for all caches. 
        --raw-cache-dir <dir>   Use alternative raw meta-data cache directory. 
        --solv-cache-dir <dir>  Use alternative solv file cache directory. 
        --pkg-cache-dir <dir>   Use alternative package cache directory. 

     Repository Options: 
        --no-gpg-checks         Ignore GPG check failures and continue. 
        --gpg-auto-import-keys  Automatically trust and import new repository 
                                signing keys. 
        --plus-repo, -p <URI>   Use an additional repository. 
        --disable-repositories  Do not read meta-data from repositories. 
        --no-refresh            Do not refresh the repositories. 
        --no-cd                 Ignore CD/DVD repositories. 
        --no-remote             Ignore remote repositories. 

     Target Options: 
        --root, -R <dir>        Operate on a different root directory. 
        --disable-system-resolvables 
                                Do not read installed packages. 

  Commands: 
        help, ?                 Print help. 
        shell, sh               Accept multiple commands at once. 

     Repository Management: 
        repos, lr               List all defined repositories. 
        addrepo, ar             Add a new repository. 
        removerepo, rr          Remove specified repository. 
        renamerepo, nr          Rename specified repository. 
        modifyrepo, mr          Modify specified repository. 
        refresh, ref            Refresh all repositories. 
        clean                   Clean local caches. 

     Service Management: 
        services, ls            List all defined services. 
        addservice, as          Add a new service. 
        modifyservice, ms       Modify specified service. 
        removeservice, rs       Remove specified service. 
        refresh-services, refs  Refresh all services. 

     Software Management: 
        install, in             Install packages. 
        remove, rm              Remove packages. 
        verify, ve              Verify integrity of package dependencies. 
        source-install, si      Install source packages and their build 
                                dependencies. 
        install-new-recommends, inr 
                                Install newly added packages recommended 
                                by installed packages. 

     Update Management: 
        update, up              Update installed packages with newer versions. 
        list-updates, lu        List available updates. 
        patch                   Install needed patches. 
        list-patches, lp        List needed patches. 
        dist-upgrade, dup       Perform a distribution upgrade. 
        patch-check, pchk       Check for patches. 

     Querying: 
        search, se              Search for packages matching a pattern. 
        info, if                Show full information for specified packages. 
        patch-info              Show full information for specified patches. 
        pattern-info            Show full information for specified patterns. 
        product-info            Show full information for specified products. 
        patches, pch            List all available patches. 
        packages, pa            List all available packages. 
        patterns, pt            List all available patterns. 
        products, pd            List all available products. 
        what-provides, wp       List packages providing specified capability. 

     Package Locks: 
        addlock, al             Add a package lock. 
        removelock, rl          Remove a package lock. 
        locks, ll               List current package locks. 
        cleanlocks, cl          Remove unused locks. 

     Other Commands: 
        versioncmp, vcmp        Compare two version strings. 
        targetos, tos           Print the target operating system ID string. 
        licenses                Print report about licenses and EULAs of 
                                installed packages. 
        source-download         Download source rpms for all installed packages 
                                to a local directory. 

Type 'zypper help <command>' to get command-specific help.
```

