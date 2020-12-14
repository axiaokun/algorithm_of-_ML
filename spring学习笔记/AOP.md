# AOP

## 背景

* 代码混乱：越来越多的非业务需求(日志和验证等)加入后，原有的业务方法急剧膨胀。每个方法在处理核心逻辑的同时还必须兼顾其他多个关注点。
* 代码分散: 以日志需求为例，只是为了满足这个单一需求，就不得不在多个模块（方法）里多次重复相同的日志代码。如果日志需求发生变化，必须修改所有模块。

## 动态代理

代理设计模式的原理：**使用一个代理将对象包装起来**，然后用该代理对象”取代”原始对象。任何对原始对象的调用都要通过代理。代理对象决定是否以及何时将方法调用转到原始对象上。

![](https://github.com/axiaokun/algorithm_of-_ML/blob/master/spring%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/image/%E5%8A%A8%E6%80%81%E4%BB%A3%E7%90%86%E7%BB%93%E6%9E%84%E5%9B%BE.png)

里面的计算器相当于真正的功能类



如何实现代理：

* 基于接口实现动态代理： JDK动态代理
* 基于继承实现动态代理： Cglib、Javassist动态代理

基于接口实现动态代理：

* 首先确定要被代理的实例对象，我们这里给出了一个简单的接口和实现类

  ```java
  //HelloInterface.java文件
  package com.atguigu.selfproxy;
  
  public interface HelloInterface {
  	void sayHello();
  }
  ```

  ```java
  //HelloImpl.java文件
  package com.atguigu.selfproxy;
  
  public class HelloImpl implements HelloInterface{
  	@Override
  	public void sayHello() {
  		System.out.println("Hello 动态代理");
  	}
  }
  ```

* 构建一个handler类来实现InvocationHandler接口

  ```java
  // ProxyHandler.java 文件
  package com.atguigu.selfproxy;
  
  import java.lang.reflect.InvocationHandler;
  import java.lang.reflect.Method;
  
  public class ProxyHandler implements InvocationHandler{
  	
  	private Object object;
  
  	public ProxyHandler(Object object) {
  		super();
  		this.object = object;
  	}
  
  	@Override
  	public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
  		System.out.println("Before invoke " + method.getName());
  		method.invoke(object, args);
  		System.out.println("After invoke " + method.getName());
  		return null;
  	}
  	
  }
  ```

* 执行动态代理：

  1. 获得被代理对象
  2. 实现InvocationHandler接口的实例对象
  3. 传入目标类加载器、目标接口、InvocationHandler为目标接口生成代理类及代理对象

  例子：

  ```java
  // Test.java文件
  package com.atguigu.selfproxy;
  
  import java.lang.reflect.InvocationHandler;
  import java.lang.reflect.Proxy;
  
  public class Test {
  	public static void main(String[] args) {
  		//JDK动态代理生成的class文件保存到本地
  		System.getProperties().setProperty("sun.misc.ProxyGenerator.saveGeneratedFiles", "true");
          //被代理对象
  		HelloInterface hello = new HelloImpl();
          //实现InvocationHandler接口的实例对象
  		InvocationHandler handler = new ProxyHandler(hello);
  		// 动态生成代理类，只需要传入目标类加载器、目标接口、InvocationHandler就可以为目标接口生成代理类及代理对象
  		HelloInterface proxyHello = (HelloInterface) Proxy.newProxyInstance(hello.getClass().getClassLoader(), hello.getClass().getInterfaces(), handler);
          //调用被代理对象的方法检测
  		proxyHello.sayHello();
  	}
  }
  /*
  输出：
  Before invoke sayHello
  Hello 动态代理
  After invoke sayHello
  */
  ```

  [动态代理的底层实现原理](https://www.jianshu.com/p/9bcac608c714)

## 什么是AOP

AOP面向切面编程，是一种新的方法论，是对OOP面向对象编程的一种补充

AOP的关注点主要是切面，作用于模块化横切关注点（即公共功能）

优点：

* 每个事物逻辑位于一个位置，代码不分散，便于维护和升级
* 业务模块更简洁，只包含核心业务代码

![](https://github.com/axiaokun/algorithm_of-_ML/blob/master/spring%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/image/AOP%E7%A4%BA%E6%84%8F%E5%9B%BE.png)

### AOP术语

* 横切关注点

  从每个方法中抽出的同一类非业务的代码

* 切面（Aspect）

  封装横切关注点信息的类，每个关注点体现为一个通知方法。

* 通知（Advice）

  切面必须要完成的各个具体工作

* 目标（Target）

  被通知的对象

* 代理（Proxy）

  向目标对象应用通知之后创建的代理对象

* 连接点（Joinpoint）

  横切关注点在程序代码中的具体体现，对应程序执行的某个特定位置。例如：类某个方法调用前、调用后、方法捕获到异常后等。

  在应用程序中可以使用横纵两个坐标来定位一个具体的连接点

* 切入点（pointcut）

  定位连接点的方式。每个类的方法中都包含多个连接点，所以连接点是类中客观存在的事物。如果把连接点看作数据库中的记录，那么切入点就是查询条件——AOP可以通过切入点定位到特定的连接点。切点通过org.springframework.aop.Pointcut 接口进行描述，它使用类和方法作为连接点的查询条件

![](image\AOP术语.png)

## 使用spring中的AOP

背景：AspectJ是Java社区里最完整最流行的AOP框架。在Spring2.0以上版本中，可以使用基于AspectJ注解或基于XML配置的AOP。

步骤：

* 导包

  ```txt
  com.springsource.net.sf.cglib-2.2.0.jar
  
  com.springsource.org.aopalliance-1.0.0.jar
  
  com.springsource.org.aspectj.weaver-1.6.8.RELEASE.jar
  
  spring-aop-4.0.0.RELEASE.jar
  
  spring-aspects-4.0.0.RELEASE.jar
  ```

* xml中引入aop名称空间

  ![](image\引入aop名称空间.png)

* 配置

  在xml文件中配置：

  ```xml
  <aop:aspectj-autoproxy />
  <!--当Spring IOC容器侦测到bean配置文件中的<aop:aspectj-autoproxy>元素时，会自动为	与AspectJ切面匹配的bean创建代理-->
  ```

* 使用注解将封装横切关注点信息的类声明为切面 

  ```java
  /*
  	1. 使用注解将作为切面的类声明为springIOC管理的bean
  	2. 使用注解将该bean声明为AspectJ切面（可以设定切面作用的优先级，如果有多个切面作用下，值越小优先级越高，默认值为int的最大值）
  	3. 设置切面包含的通知的通知类型
  	   AspectJ支持5种类型的通知注解有：
  	   1. @Before：前置通知，在方法执行之前执行
  	   2. @After：后置通知，在方法执行之后执行
  	   3. @AfterRunning：返回通知，在方法返回结果之后执行
  	   4. @AfterThrowing：异常通知，在方法抛出异常之后执行
  	   5. @Around：环绕通知，围绕着方法执行
  */
  
  package com.atguigu.spring.aop;
  
  import java.util.Arrays;
  
  import org.aspectj.lang.JoinPoint;
  import org.aspectj.lang.ProceedingJoinPoint;
  import org.aspectj.lang.annotation.After;
  import org.aspectj.lang.annotation.AfterReturning;
  import org.aspectj.lang.annotation.AfterThrowing;
  import org.aspectj.lang.annotation.Around;
  import org.aspectj.lang.annotation.Aspect;
  import org.aspectj.lang.annotation.Before;
  import org.aspectj.lang.annotation.Pointcut;
  import org.springframework.core.annotation.Order;
  import org.springframework.stereotype.Component;
  
  @Component
  @Aspect//标注当前类为切面
  @Order(1)//定义切面作用的优先级，值越小优先级越高，默认值为int的最大值
  public class MyloggerAspect {
  	
  	@Pointcut(value="execution(* com.atguigu.spring.aop.*.*(..))")
  	public void test() {}
  
  	/**
  	 * @Before:将方法指定为前置通知
  	 * 必须设置value，其值为切入点表达式
  	 * 前置通知：作用于方法执行之前
  	 * @Before(value="execution(* com.atguigu.spring.aop.*.*(..))")
  	 * 第一个*代表任意的访问修饰符和返回值类型
  	 * 第二个*代表任意类
  	 * 第三个*代表类中任意方法
  	 * ..代表任意的参数列表
  	 */
  	//@Before(value = "execution(public int com.atguigu.spring.aop.MathImpl.add(int, int))")
  	@Before(value="test()")
  	public void beforeMethod(JoinPoint joinPoint) {
  		Object[] args = joinPoint.getArgs();//获取方法的参数
  		String methodName = joinPoint.getSignature().getName();//获取方法名
  		System.out.println("method:"+methodName+",arguments:"+Arrays.toString(args));
  	}
  	
  	/**
  	 * @After:将方法标注为后置通知
  	 * 后置通知：作用于方法的finally语句块，即不管有没有异常都会执行
  	 */
  	//@After(value="execution(* com.atguigu.spring.aop.*.*(..))")
  	@After(value="test()")
  	public void afterMethod() {
  		System.out.println("后置通知");
  	}
  	
  	/**
  	 * @AfterReturning:将方法标注为返回通知
  	 * 返回通知：作用于方法执行之后
  	 * 可通过returning设置接收方法返回值的变量名
  	 * 要想在方法中使用，必须在方法的形参中设置和变量名相同的参数名的参数
  	 */
  	//@AfterReturning(value="execution(* com.atguigu.spring.aop.*.*(..))", returning="result")
  	@AfterReturning(value="test()", returning="result")
  	public void afterReturningMethod(JoinPoint joinPoint, Object result) {
  		String methodName = joinPoint.getSignature().getName();
  		System.out.println("method:"+methodName+",result:"+result);
  	}
  	
  	/**
  	 * @AfterThrowing:将方法标注为异常通知（例外通知）
  	 * 异常通知（例外通知）:作用于方法抛出异常时
  	 * 可通过throwing设置接收方法返回的异常信息
  	 * 在参数列表中课通过具体的异常类型，来对指定的异常信息进行操作
  	 */
  	//@AfterThrowing(value="execution(* com.atguigu.spring.aop.*.*(..))", throwing="ex")
  	@AfterThrowing(value="test()", throwing="ex")
  	public void afterThrowingMethod(ArithmeticException ex) {
  		System.out.println("有异常了，messages："+ex);
  	}
  	
  	
  	/*@Around(value="execution(* com.atguigu.spring.aop.*.*(..))")
  	public Object aroundMethod(ProceedingJoinPoint joinPoint) {
  		
  		Object result = null;
  		
  		try {
  			//前置通知
  			System.out.println("前置通知");
  			result = joinPoint.proceed();//执行方法
  			//返回通知
  			System.out.println("返回通知");
  			return result;
  		} catch (Throwable e) {
  			// TODO Auto-generated catch block
  			e.printStackTrace();
  			//异常通知
  			System.out.println("异常通知");
  		} finally {
  			//后置通知
  			System.out.println("后置通知");
  		}
  		
  		return -1;
  	}*/
  }
  
  ```

  



























