#ifndef _CATALOG_COMMANDS_HPP
#define _CATALOG_COMMANDS_HPP

#include "api/catalog/catalog.hpp"

#include <memory>

#include "api/registry.hpp"

namespace api::catalog::cmds
{

api::CommandFn postResourceCmd(std::shared_ptr<Catalog> catalog);
api::CommandFn getResourceCmd(std::shared_ptr<Catalog> catalog);
api::CommandFn deleteResourceCmd(std::shared_ptr<Catalog> catalog);
api::CommandFn putResourceCmd(std::shared_ptr<Catalog> catalog);
api::CommandFn validateResourceCmd(std::shared_ptr<Catalog> catalog);

/**
 * @brief Register all available Catalog commands in the API registry.
 *
 * @param catalog Catalog to use
 * @param registry API registry
 * @throw std::runtime_error If the command registration fails for any reason and at any
 * point
 */
void registerAllCmds(std::shared_ptr<Catalog> catalog,
                     std::shared_ptr<api::Registry> registry);

} // namespace api::catalog::cmds

#endif // _CATALOG_COMMANDS_HPP