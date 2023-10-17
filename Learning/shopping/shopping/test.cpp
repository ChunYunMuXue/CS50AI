#include <iostream>
#include <algorithm>
#include <iomanip>

using namespace std;

int main()
{
    double G,B,R,V,S,H,max0,min0;
    cin>>R>>G>>B;
    R=R/255;
    G=G/255;
    B=B/255;
    max0=max(R,max(G,B));
    V=max0;
    min0=min(R,max(G,B));
if(V==0){S=0;}
else{S=(max0-min0)/max0;}
if(max0!=min0){
if(max0==R) H=60*(0+(G-B)/(max0-min0));
if(max0==G) H=60*(2+(B-R)/(max0-min0));
if(max0==B) H=60*(4+(R-G)/(max0-min0));
if(H<0) H=H+360;
}
else{H=0;}
cout<<fixed;
cout<<setprecision(4)<<H<<','<<S*100<<'%'<<','<<V*100<<'%'<<endl;

    return 0;
}