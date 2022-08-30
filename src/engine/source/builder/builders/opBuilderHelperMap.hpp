/* Copyright (C) 2015-2022, Wazuh Inc.
 * All rights reserved.
 *
 * This program is free software; you can redistribute it
 * and/or modify it under the terms of the GNU General Public
 * License (version 2) as published by the FSF - Free Software
 * Foundation.
 */

#ifndef _OP_BUILDER_HELPER_MAP_H
#define _OP_BUILDER_HELPER_MAP_H

#include <any>

#include <baseTypes.hpp>

#include "expression.hpp"
#include <utils/stringUtils.hpp>
/*
 * The helper Map (Transformation), builds a lifter that will chain rxcpp map operation
 * Rxcpp transform expects a function that returns event.
 */

namespace builder::internals::builders
{

//*************************************************
//*           String tranform                     *
//*************************************************

/**
 * @brief Transforms a string to uppercase and append or remplace it in the event `e`
 *
 * @param definition The transformation definition. i.e : `<field>: +s_up/<str>|$<ref>`
 * @return base::Expression The lifter with the `uppercase` transformation.
 * @throw std::runtime_error if the parameter is not a string.
 */
base::Expression opBuilderHelperStringUP(const std::any& definition);

/**
 * @brief Transforms a string to lowercase and append or remplace it in the event `e`
 *
 * @param definition The transformation definition. i.e : `<field>: +s_lo/<str>|$<ref>`
 * @return base::Expression The lifter with the `lowercase` transformation.
 * @throw std::runtime_error if the parameter is not a string.
 */
base::Expression opBuilderHelperStringLO(const std::any& definition);

/**
 * @brief Transforms a string, trim it and append or remplace it in the event `e`
 *
 * @param definition The transformation definition.
 * i.e : `<field>: +s_trim/[begin | end | both]/char`
 * @return base::Expression The lifter with the `trim` transformation.
 * @throw std::runtime_error if the parameter is not a string.
 */
base::Expression opBuilderHelperStringTrim(const std::any& definition);

/**
 * @brief Transform a list of arguments into a single strim with all of them concatenated
 *
 * @param def The transformation definition.
 * i.e : '<field>: +s_concat/<stringA>|$<referenceA>/<stringB>|$<referenceB>/...'
 * @return base::Expression The lifter with the `concat` transformation.
 */
base::Expression opBuilderHelperStringConcat(const std::any& definition);

/**
 * @brief Transforms an array of strings into a single string field result of concatenate
 * them with a separator between (not at the start or the end).
 * i.e: '<field>: +s_fromArray/$<array_reference1>/<separator>'
 * @param definition The transformation definition.
 * @throw std::runtime_error if the parameter is not a reference or if theres no
 * Value argument for the separator.
 * @return base::Expression
 */
base::Expression opBuilderHelperStringFromArray(const std::any& definition);

//*************************************************
//*           Int tranform                        *
//*************************************************

/**
 * @brief Transforms an integer. Performs a mathematical operation on an event field.
 *
 * @param definition The transformation definition.
 * i.e : `<field>: +i_calc/[sum|sub|mul|div]/[value|$<ref>]`
 * @return base::Expression The lifter with the `mathematical operation` transformation.
 * @throw std::runtime_error if the parameter is not a integer.
 */
base::Expression opBuilderHelperIntCalc(const std::any& definition);

//*************************************************
//*             JSON tranform                     *
//*************************************************

// <field>: +delete_field/
/**
 * @brief Delete a field of the json event
 *
 * @param def The transformation definition.
 * i.e : '<field>: +delete_field/<string1>/<string2>'
 * @return base::Expression The lifter with the `delete_field` transformation.
 */
base::Expression opBuilderHelperDeleteField(const std::any& definition);

//*************************************************
//*           Regex tranform                      *
//*************************************************

/**
 * @brief Builds regex extract operation.
 * Maps into an auxiliary field the part of the field value that matches a regexp
 *
 * @param definition Definition of the operation to be built
 * @return base::Expression The lifter with the `regex extract` transformation.
 * @throw std::runtime_error if the parameter is the regex is invalid.
 */
base::Expression opBuilderHelperRegexExtract(const std::any& definition);

//*************************************************
//*           Array tranform                      *
//*************************************************

/**
 * @brief Append string to array field.
 * Accepts parameters with literals or references. If reference not exists or is not an
 * string it will fail.
 *
 * @param definition Definition of the operation to be built
 * @return base::Expression The lifter with the `append string to array` transformation.
 * @throw std::runtime_error if the parameters are empty.
 */
base::Expression opBuilderHelperAppendString(const std::any& definition);


/**
 * @brief Append splitted strings to array field.
 * Accepts one parameter with a reference and another with seprator char. If reference not
 * exists, is not a string or split operation fails it will fail.
 *
 * @param definition Definition of the operation to be built
 * @return base::Expression The lifter with the `append splitted strings to array`
 * transformation.
 * @throw std::runtime_error if the parameters size is not 2 or character separator is not
 * valid.
 */
base::Expression opBuilderHelperAppendSplitString(const std::any& definition);

//*************************************************
//*              IP tranform                      *
//*************************************************
/**
 * @brief Get the Internet Protocol version of an IP address.
 *
 * @param definition The transformation definition.
 * @return base::Expression The lifter with the `ip version` transformation.
 */
base::Expression opBuilderHelperIPVersionFromIPStr(const std::any& definition);

} // namespace builder::internals::builders

#endif // _OP_BUILDER_HELPER_MAP_H