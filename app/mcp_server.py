"""MCP tools for trusted local/stdio clients only. Server-enforced scopes.
Do not expose this stdio server as a public network service.
"""
from mcp.server.fastmcp import FastMCP
from app.analytics import sales_summary,low_stock,stock_movements
from app.security import Principal
import os
mcp=FastMCP('retailai-demo')
def principal():
    return Principal(role=os.getenv('DEMO_ROLE','analyst'),
        countries=[s.strip() for s in os.getenv('DEMO_ALLOWED_COUNTRIES','France').split(',') if s.strip()],
        brands=[s.strip() for s in os.getenv('DEMO_ALLOWED_BRANDS','Casanoov,Cazeboo,Sicaan').split(',') if s.strip()])
@mcp.tool()
def get_sales_summary(group_by:str='marque')->list[dict]:
    """Aggregated synthetic sales restricted to server-authorized brands/countries."""
    u=principal()
    return sales_summary(group_by,countries=u.countries,brands=u.brands)
@mcp.tool()
def get_low_stock(threshold:int=15)->list[dict]:
    """Observed synthetic low-stock records restricted to authorized brands."""
    return low_stock(threshold,brands=principal().brands)
@mcp.tool()
def get_stock_movements()->list[dict]:
    """Net movements, restricted to demo admin role."""
    if principal().role!='admin':
        raise PermissionError('Admin role required')
    return stock_movements()
if __name__=='__main__':mcp.run()
