from inspect import getmodule, stack

### Helps with graph IDs
## Dash requires unique IDs for the entire app. Reduce mental overhead by 
## generating IDs with module names appended, effectively making IDs
## appear local to module.

def init_ids(names):
    results = {}
    callingModule = getmodule(stack()[1][0])
    for name in names:
        ## Replace '.' with '_' because IDs may not have '.' in Dash
        results[name] = name + '--' + callingModule.__name__.replace('.', '_')
    return results
