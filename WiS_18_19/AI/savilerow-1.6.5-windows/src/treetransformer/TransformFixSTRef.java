package savilerow.treetransformer;
/*

    Savile Row http://savilerow.cs.st-andrews.ac.uk/
    Copyright (C) 2014-2017 Peter Nightingale
    
    This file is part of Savile Row.
    
    Savile Row is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    Savile Row is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with Savile Row.  If not, see <http://www.gnu.org/licenses/>.

*/


import savilerow.expression.*;
import savilerow.model.*;

import java.util.*;

public class TransformFixSTRef extends TreeTransformerBottomUpNoWrapper
{
    SymbolTable st;
    public TransformFixSTRef(SymbolTable _st) {
        super(null);
        st=_st;
    }
    
	protected NodeReplacement processNode(ASTNode curnode)
	{
	    if(curnode instanceof Identifier && ((Identifier)curnode).global_symbols!=st) {
	        return new NodeReplacement(new Identifier(curnode.toString(), st));
	    }
	    return null;
	}
}
