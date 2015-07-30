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

#include "graph_python_interface.hh"
#include "graph_filtering.hh"
#include "graph.hh"
#include "graph_selectors.hh"
#include "graph_properties.hh"

#include <boost/bind.hpp>
#include <boost/bind/placeholders.hpp>
#include <boost/mpl/push_back.hpp>
#include <boost/python.hpp>

#include "graph_community_network.hh"

using namespace std;
using namespace boost;

using namespace graph_tool;

typedef ConstantPropertyMap<int32_t,GraphInterface::edge_t> no_eweight_map_t;
typedef ConstantPropertyMap<int32_t,GraphInterface::vertex_t> no_vweight_map_t;
typedef property_map_type::apply<int32_t,GraphInterface::edge_index_map_t>::type::unchecked_t ecount_map_t;
typedef property_map_type::apply<int32_t,GraphInterface::vertex_index_map_t>::type::unchecked_t vcount_map_t;

struct get_community_network_vertices_dispatch
{
    template <class Graph, class CommunityGraph, class CommunityMap,
              class VertexWeightMap>
    void operator()(const Graph& g, CommunityGraph& cg,
                    CommunityMap s_map, boost::any acs_map,
                    VertexWeightMap vweight, boost::any vcount) const
    {
        typename CommunityMap::checked_t cs_map = boost::any_cast<typename CommunityMap::checked_t>(acs_map);

        typedef typename boost::mpl::if_<std::is_same<no_vweight_map_t, VertexWeightMap>,
                                         vcount_map_t, VertexWeightMap>::type vweight_t;
        typename vweight_t::checked_t vertex_count = boost::any_cast<typename vweight_t::checked_t>(vcount);

        get_community_network_vertices()(g, cg, s_map, cs_map, vweight, vertex_count);
    }

};

struct get_community_network_edges_dispatch
{
    get_community_network_edges_dispatch(bool self_loops): _self_loops(self_loops) {}
    bool _self_loops;

    template <class Graph, class CommunityGraph, class CommunityMap,
              class EdgeWeightMap, class EdgeIndex>
    void operator()(const Graph& g, CommunityGraph& cg, EdgeIndex cedge_index,
                    CommunityMap s_map, boost::any acs_map,
                    EdgeWeightMap eweight, boost::any ecount) const
    {
        typename CommunityMap::checked_t cs_map = boost::any_cast<typename CommunityMap::checked_t>(acs_map);

        typedef typename boost::mpl::if_<std::is_same<no_eweight_map_t, EdgeWeightMap>,
                                         ecount_map_t, EdgeWeightMap>::type eweight_t;

        typename eweight_t::checked_t edge_count = boost::any_cast<typename eweight_t::checked_t>(ecount);
        get_community_network_edges()(g, cg, cedge_index, s_map,
                                      cs_map, eweight, edge_count,
                                      _self_loops);
    }
};

void community_network_edges(GraphInterface& gi, GraphInterface& cgi,
                             boost::any community_property,
                             boost::any condensed_community_property,
                             boost::any edge_count, boost::any eweight,
                             bool self_loops, bool parallel_edges);

void community_network(GraphInterface& gi, GraphInterface& cgi,
                       boost::any community_property,
                       boost::any condensed_community_property,
                       boost::any vertex_count, boost::any edge_count,
                       boost::any vweight, boost::any eweight, bool self_loops,
                       bool parallel_edges)
{
    typedef boost::mpl::push_back<writable_vertex_scalar_properties, no_vweight_map_t>::type
        vweight_properties;

    if (vweight.empty())
        vweight = no_vweight_map_t(1);

    run_action<>()
        (gi, std::bind(get_community_network_vertices_dispatch(),
                       placeholders::_1, std::ref(cgi.GetGraph()),
                       placeholders::_2, condensed_community_property,
                       placeholders::_3, vertex_count),
         writable_vertex_properties(), vweight_properties())
        (community_property, vweight);

    community_network_edges(gi, cgi, community_property,
                            condensed_community_property, edge_count,
                            eweight, self_loops, parallel_edges);
}
