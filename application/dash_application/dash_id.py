from inspect import getmodule, stack

### Helps with graph IDs
## Dash requires unique IDs for the entire app. Reduce mental overhead by 
## generating IDs with module names appended, effectively making IDs
## appear local to module.

## Optional parameter allows developer to define name appended to ID
## rather than automatically getting the name of the calling module.
## This introduces the danger of the developer setting the same name
## twice, which will cause Dash to cease correct rendering of pages
## due to ID conflict. Please use carefully.
def init_ids(names, moduleName=None):
    results = {}
    if not moduleName:
        callingModule = getmodule(stack()[1][0])
        moduleName = callingModule.__name__
    for name in names:
        ## Replace '.' with '_' because IDs may not have '.' in Dash
        results[name] = name + '--' + moduleName.replace('.', '_')
    return results
