// graph-tool -- a general graph modification and manipulation thingy
//
// Copyright (C) 2006-2015 Tiago de Paula Peixoto <tiago@skewed.de>
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 3
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <http://www.gnu.org/licenses/>.

#include "graph.hh"
#include "graph_filtering.hh"

#include "graph_union.hh"

#include <boost/bind.hpp>

#include <boost/python/extract.hpp>

using namespace graph_tool;
using namespace boost;

typedef property_map_type::apply<int64_t,
                                 GraphInterface::vertex_index_map_t>::type
    vprop_t;

typedef property_map_type::apply<GraphInterface::edge_t,
                                 GraphInterface::edge_index_map_t>::type
    eprop_t;

struct get_pointers
{
    template <class List>
    struct apply
    {
        typedef typename boost::mpl::transform<List,
                                               boost::mpl::quote1<std::add_pointer> >::type type;
    };
};

boost::python::tuple graph_union(GraphInterface& ugi, GraphInterface& gi,
                                 boost::any avprop)
{
    vprop_t vprop = boost::any_cast<vprop_t>(avprop);
    eprop_t eprop(gi.GetEdgeIndex());
    run_action<graph_tool::detail::always_directed,boost::mpl::true_>()
        (ugi, std::bind(graph_tool::graph_union(),
                        placeholders::_1, placeholders::_2, vprop, eprop),
         get_pointers::apply<graph_tool::detail::always_directed>::type())
        (gi.GetGraphView());
    return boost::python::make_tuple(avprop, boost::any(eprop));
}
